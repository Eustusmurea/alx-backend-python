from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from .models import Message, User
from .serializers import MessageSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threaded_conversations(request):
    root_messages = (
        Message.objects
        .filter(parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver').all())
        )
    )
    serializer = MessageSerializer(root_messages, many=True)
    return Response(serializer.data)


threaded_conversations = cache_page(60)(threaded_conversations)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    data = request.data
    try:
        message = Message.objects.create(
            sender=request.user,
            receiver_id=data.get('receiver'),
            content=data.get('content'),
            parent_message_id=data.get('parent_message')
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages(request):
    user = request.user
    unread_messages = Message.unread_messages.for_user(user) 
    serializer = MessageSerializer(unread_messages, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"message": "User and all related data deleted successfully."}, status=status.HTTP_200_OK)
