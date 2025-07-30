from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Message, User
from .serializers import MessageSerializer
from django.db.models import Prefetch

@api_view(['GET'])
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

@api_view(['DELETE'])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"message": "User and all related data deleted successfully."})

