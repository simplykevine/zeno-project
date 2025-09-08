from rest_framework import serializers
from users.models import User, Review
from agents.models import Agent, Tool



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