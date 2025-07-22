from rest_framework.permissions import BasePermission

class IsParticipant(BasePermission):
    """
    Custom permission to only allow participants of a chat to access it.

    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            # Check if the user is a participant in the conversation
            return request.user in obj.participants.all()
        
        if hasattr(obj, 'conversation'):
            # If the object is a message, check if the user is a participant in the conversation
            return request.user in obj.conversation.participants.all()
        
        

class IsSender(BasePermission):
    """
    Custom permission to only allow the sender of a message to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user
