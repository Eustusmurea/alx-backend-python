from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)


class IsParticipant(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        logger.debug(f"Checking permission for user: {request.user}, Authenticated: {request.user.is_authenticated}")
        logger.debug(f"Request headers: {request.headers}")
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            logger.debug(f"Checking if user {request.user} is a participant in conversation {obj}")
            return request.user in obj.participants.all()

        if hasattr(obj, 'conversation'):
            logger.debug(f"Checking if user {request.user} is a participant in message's conversation {obj.conversation}")
            return request.user in obj.conversation.participants.all()

        logger.warning(f"Object {obj} has no 'participants' or 'conversation' attribute")
        return False


class IsSender(permissions.BasePermission):
    """
    Allows only the sender of a message to update or delete it.
    Allows safe methods (GET, HEAD, OPTIONS) for participants.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read access to participants

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            is_sender = hasattr(obj, 'sender') and obj.sender == request.user
            logger.debug(f"Checking if user {request.user} is sender of message {obj}: {is_sender}")
            return is_sender

        return False