from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'replies']

    def get_replies(self, obj):
        children = obj.replies.all()
        return MessageSerializer(children, many=True, context=self.context).data
