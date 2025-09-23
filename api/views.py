from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from users.models import User, Review
from agents.models import Agent, Tool
from runs.models import Run, RunInputFile, RunOutputArtifact 
from conversations.models import Conversation, Step
from .serializers import UserSerializer, ReviewSerializer, AgentSerializer, ConversationSerializer, ToolSerializer, StepSerializer, RunInputFileSerializer, RunOutputArtifactSerializer, RunSerializer, ConversationWithRunsSerializer
from .permissions import IsAdmin
import threading, time, random

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def with_runs(self, request):
        user = request.user
        user_id = request.query_params.get('user_id')

        queryset = Conversation.objects.all()

        if user_id:
            if IsAdmin().has_permission(request, self):
                queryset = queryset.filter(user_id=user_id)
            else:
                return Response(
                    {"error": "You are not allowed to fetch other users' conversations."},
                    status=403
                )
        else:
            queryset = queryset.filter(user=user)

        queryset = queryset.order_by('-created_at')[:10]

        queryset = queryset.prefetch_related('runs__input_files', 'runs__output_artifacts')

        serializer = ConversationWithRunsSerializer(queryset, many=True)
        return Response(serializer.data)


class RegisterView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'User registered successfully',
                'token': token.key,
                'role': getattr(user, 'role', None)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "id": user.id,
            "email": user.email,
            "role": user.role
        })


class LogoutView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role.lower() == "admin":
            return Review.objects.all()
        else:
            return Review.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.role.lower() != "admin":
            return Response({"error": "You do not have permission to delete reviews"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user, 'role', '').lower()

        if role == 'admin':
            return User.objects.all()
        elif role == 'user':
            return User.objects.filter(id=user.id)
        else:
            return User.objects.none()

    def perform_update(self, serializer):
        user = self.request.user
        role = getattr(user, 'role', '').lower()

        if role == 'admin' or user.id == serializer.instance.id:
            serializer.save()
        else:
            raise PermissionDenied({"error": "You do not have permission to update this user."})
    def perform_destroy(self, instance):
        user = self.request.user
        role = getattr(user, 'role', '').lower()

        if role == 'admin' or user.id == instance.id:
            instance.delete()
        else:
            raise PermissionDenied({"error": "You do not have permission to delete this user."})
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    lookup_field = 'agent_id'
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all().order_by('tool_name')
    serializer_class = ToolSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdmin]  


class StepViewSet(viewsets.ModelViewSet):
    serializer_class = StepSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role.lower() == "admin":
            return Step.objects.select_related('conversation', 'tool', 'agent').all()
        else:
            return Step.objects.filter(
                conversation__user=user
            ).select_related('conversation', 'tool', 'agent')

    @action(detail=False, methods=['get'])
    def by_conversation(self, request):
        conversation_id = request.query_params.get('conversation_id')
        if not conversation_id:
            return Response({"error": "conversation_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        steps = self.get_queryset().filter(conversation_id=conversation_id).order_by('step_order')
        serializer = self.get_serializer(steps, many=True)
        return Response(serializer.data)
    

class RunViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]

    def create(self, request):
        user_input = request.data.get('user_input', '').strip()
        conversation_id = request.data.get('conversation_id', None)

        if not user_input:
            return Response({'error': 'user_input required'}, status=400)

        conversation = None
        if conversation_id:
            try:
                conversation = Conversation.objects.get(conversation_id=conversation_id)
                if conversation.user:
                    if not request.user.is_authenticated:
                        return Response(
                            {'error': 'Login required to use this conversation'},
                            status=status.HTTP_403_FORBIDDEN
                        )
                    if conversation.user != request.user:
                        return Response(
                            {'error': 'Not allowed to use this conversation'},
                            status=status.HTTP_403_FORBIDDEN
                        )
            except Conversation.DoesNotExist:
                return Response({'error': 'Conversation not found'}, status=404)

        run = Run.objects.create(
            user_input=user_input,
            conversation=conversation,
            status='pending'
        )

        files = request.FILES.getlist('files')
        for file in files:
            if file.name.endswith('.pdf'):
                file_type = 'pdf'
            elif file.name.endswith('.csv'):
                file_type = 'csv'
            else:
                file_type = 'text'

            RunInputFile.objects.create(
                run=run,
                file=file,
                file_type=file_type,
                description=f"Uploaded {file_type} file"
            )

        RunOutputArtifact.objects.create(
            run=run,
            artifact_type='chart',
            data={
                "chart_type": "line",
                "x": [2024, 2025, 2026],
                "y": [random.randint(100, 200) for _ in range(3)],
                "title": "Trade Forecast"
            },
            title="Export Forecast Chart"
        )
        RunOutputArtifact.objects.create(
            run=run,
            artifact_type='table',
            data={
                "columns": ["Year", "Value"],
                "rows": [
                    [2024, 120],
                    [2025, 135],
                    [2026, 150]
                ]
            },
            title="Export Data Table"
        )

        run.status = Run.COMPLETED
        run.save(update_fields=['status'])

        serializer = RunSerializer(run)
        return Response(serializer.data, status=201)

    def list(self, request):
        user = request.user
        if user.role.lower() == 'admin':
            queryset = Run.objects.all()
        else:
            queryset = Run.objects.filter(conversation__user=user)

        serializer = RunSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            run = Run.objects.get(id=pk)
        except Run.DoesNotExist:
            return Response({'error': 'Run not found'}, status=404)

        if run.conversation and run.conversation.user != request.user:
            return Response({'error': 'Not authorized to view this run'}, status=403)

        serializer = RunSerializer(run)
        return Response(serializer.data)

    def simulate_status(self, run_id):
        try:
            run = Run.objects.get(id=run_id)
            run.status = 'running'
            run.save(update_fields=['status'])

            RunOutputArtifact.objects.create(
                run=run,
                artifact_type='chart',
                data={
                    "chart_type": "line",
                    "x": [2024, 2025, 2026],
                    "y": [random.randint(100, 200) for _ in range(3)],
                    "title": "Trade Forecast"
                },
                title="Export Forecast Chart"
            )

            RunOutputArtifact.objects.create(
                run=run,
                artifact_type='table',
                data={
                    "columns": ["Year", "Value"],
                    "rows": [
                        [2024, 120],
                        [2025, 135],
                        [2026, 150]
                    ]
                },
                title="Export Data Table"
            )

            run.status = 'completed'
            run.save(update_fields=['status'])

        except Exception:
            pass


