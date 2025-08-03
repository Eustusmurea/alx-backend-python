from django.db import models
from django.db.models import Q

class MessageManager(models.Manager):
    """Custom manager for Message model with conversation queries"""
    def get_conversation(self, message):
        """Get entire conversation thread starting from a message"""
        return self.filter(
            Q(id=message.id) |
            Q(parent_message=message.id) |
            Q(parent_message__parent_message=message.id)
        ).select_related('sender', 'receiver', 'parent_message').only(
            'id', 'content', 'timestamp', 'sender__username', 
            'receiver__username', 'parent_message_id', 'read'
        )

    def get_user_conversations(self, user):
        """Get all conversation threads for a user"""
        return self.filter(
            Q(sender=user) | Q(receiver=user)
        ).select_related('sender', 'receiver').only(
            'id', 'content', 'timestamp', 'sender__username',
            'receiver__username', 'read'
        ).order_by('-timestamp')

class UnreadMessagesManager(models.Manager):
    """Custom manager for unread messages"""
    def for_user(self, user):
        """Returns unread messages for a specific user with optimized queries"""
        return self.filter(
            receiver=user,
            read=False
        ).select_related('sender').only(
            'id', 'content', 'timestamp', 'sender__username', 'sender__id'
        )

    def count_for_user(self, user):
        """Optimized count of unread messages for a user"""
        return self.filter(
            receiver=user,
            read=False
        ).count()

class NotificationManager(models.Manager):
    """Custom manager for Notification model"""
    def unread_for_user(self, user):
        """Get unread notifications with optimized queries"""
        return self.filter(
            user=user,
            read=False
        ).select_related('message__sender').only(
            'id', 'created_at', 'message__id', 
            'message__content', 'message__sender__username'
        )

    def mark_all_as_read(self, user):
        """Mark all notifications as read for a user"""
        return self.filter(
            user=user,
            read=False
        ).update(read=True)
    