from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing conversation instances.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with the authenticated user as a participant.
        """
        participants = request.data.get('participants', [])
        if not participants:
            return Response({"error": "At least one participant is required."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.add(*User.objects.filter(user_id__in=participants))
        conversation.participants.add(request.user)  # Ensure creator is included
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing message instances.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body']
    ordering_fields = ['sent_at']

    def create(self, request, *args, **kwargs):
        """
        Create a new message in a conversation.
        """
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response({"error": "Conversation ID and message_body are required."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.filter(conversation_id=conversation_id).first()
        if not conversation:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
