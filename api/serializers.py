from rest_framework import serializers
from users.models import User, Review
from conversations.models import Conversation
from agents.models import Agent, Tool
from conversations.models import Step 


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'image', 'created_at', 'password']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data, password=password)
        return user


class ConversationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'user', 'user_id', 'title', 'created_at']
        read_only_fields = ['conversation_id', 'created_at', 'title']

    def create(self, validated_data):
        validated_data['title'] = "New Chat"
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['review_id', 'review_text', 'rating', 'created_at', 'user']


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['agent_id', 'agent_name', 'description']

class ToolSerializer(serializers.ModelSerializer):
    tool_name = serializers.CharField(required=True, allow_blank=False)
    tool_description = serializers.CharField(required=True, allow_blank=False)
    meta_data = serializers.JSONField(required=True)

    class Meta:
        model = Tool
        fields = '__all__'

class StepSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all()
    )
    tool = serializers.PrimaryKeyRelatedField(
        queryset=Tool.objects.all(),
        required=False,
        allow_null=True
    )
    agent = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Step
        fields = [
            'step_id',
            'conversation',
            'step_order',
            'type',
            'content',
            'tool',
            'agent',
            'created_at'
        ]
        read_only_fields = ['step_id', 'created_at']

    def validate(self, data):
        step_type = data.get('type')
        tool = data.get('tool')
        agent = data.get('agent')

        if step_type == 'tool_call' and not tool:
            raise serializers.ValidationError({
                'tool': "This field is required when type is 'tool_call'."
            })
        if step_type == 'sub_agent_call' and not agent:
            raise serializers.ValidationError({
                'agent': "This field is required when type is 'sub_agent_call'."
            })

        if step_type != 'tool_call' and tool:
            raise serializers.ValidationError({
                'tool': "This field should only be set when type is 'tool_call'."
            })
        if step_type != 'sub_agent_call' and agent:
            raise serializers.ValidationError({
                'agent': "This field should only be set when type is 'sub_agent_call'."
            })

        return data

