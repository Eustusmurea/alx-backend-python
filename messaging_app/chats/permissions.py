from rest_framework.permissions import BasePermission

import logging
logger = logging.getLogger(__name__)

class IsParticipant(BasePermission):
    def has_permission(self, request, view):
        logger.debug(f"Checking permission for user: {request.user}, Authenticated: {request.user.is_authenticated}")
        logger.debug(f"Request headers: {request.headers}")
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            logger.debug(f"Checking if user {request.user} is a participant in conversation {obj}")
            return request.user in obj.participants.all()
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False
        
        

class IsSender(BasePermission):
    """
    Custom permission to only allow the sender of a message to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user
