import uuid
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant
from .filters import MessageFilter
from .pagination import MessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'conversation_id'

    def get_queryset(self):
        # Only conversations the user participates in
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    search_fields = ['message_body']
    ordering_fields = ['sent_at']
   

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_conversation_id')
        if not conversation_id:
            raise ValidationError({'error': 'Invalid or missing conversation ID.'})
        return Message.objects.filter(
            conversation__conversation_id=conversation_id,
            conversation__participants=self.request.user
        )
    

    def create(self, request, *args, **kwargs):
        conversation_id = kwargs.get('conversation_conversation_id')  # FIXED
        print(f"DEBUG: conversation_id from URL = {conversation_id}")

        # Validate UUID
        try:
            conversation_uuid = uuid.UUID(conversation_id)
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid or missing conversation ID."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retrieve the conversation
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_uuid)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Ensure user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Validate message content
        message_body = request.data.get('message_body', '').strip()
        if not message_body:
            return Response(
                {"error": "Message body is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create and return the message
        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
