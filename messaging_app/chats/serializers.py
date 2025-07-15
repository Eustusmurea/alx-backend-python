from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'content', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    Messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'Messages']

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
        fields = ['message_id', 'sender', 'sender_username', 'conversation', 'content', 'timestamp']

    def get_sender_username(self, obj):
        return obj.sender.username if obj.sender else None

    def validate_content(self, value):
        content = value.strip()  # remove leading/trailing spaces

        if not content:
            raise serializers.ValidationError("Message content cannot be empty.")
        return content


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    Messages = MessageSerializer(many=True, read_only=True)
    topic = serializers.CharField(default="General", read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'Messages', 'topic']
