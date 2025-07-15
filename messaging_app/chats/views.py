from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from rest_framework import filters


User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with selected participants.
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response(
                {"error": "At least one participant is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        # Add participants + current user
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(users | User.objects.filter(pk=request.user.pk))
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body']
    ordering_fields = ['sent_at']

    def create(self, request, *args, **kwargs):
        """
        Send a message to a conversation.
        """
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response(
                {"error": "Both conversation and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.filter(conversation_id=conversation_id).first()
        if not conversation:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
