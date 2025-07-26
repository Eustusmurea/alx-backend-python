from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_username', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender', 'sender_username', 'sent_at']

    def get_sender_username(self, obj):
        return obj.sender.username if obj.sender else None

    def validate_message_body(self, value):
        content = value.strip()
        if not content:
            raise serializers.ValidationError("Message body cannot be empty.")
        if len(content) < 5:
            raise serializers.ValidationError("Message body is too short. Minimum 5 characters required.")
        if len(content) > 500:
            raise serializers.ValidationError("Message body is too long. Maximum 500 characters allowed.")
        return content


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    Messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'Messages', 'topic']
        read_only_fields = ['conversation_id', 'participants', 'created_at', 'Messages']
