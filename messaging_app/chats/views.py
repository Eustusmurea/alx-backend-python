from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as drf_filters

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant, IsSender
from .filters import MessageFilter, ConversationFilter
from .pagination import MessagePagination

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filterset_class = ConversationFilter
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

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

        # Create a new conversation and add participants (including self)
        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(list(users) + [request.user])
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        return Message.objects.filter(conversation__participants=self.request.user)

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

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
