#sender
#receiver
#content
#timestamp

from django.db import models
from django.contrib.auth.models import User


class MessageManager(models.Manager):
    def get_conversation(self, message):
        """Get entire conversation thread starting from a message"""
        return self.filter(
            models.Q(id=message.id) |
            models.Q(parent_message=message.id) |
            models.Q(parent_message__parent_message=message.id)
        ).select_related('sender', 'receiver', 'parent_message')

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """Returns unread messages for a specific user"""
        return self.filter(
            receiver=user,
            read=False
        ).select_related('sender').only(
            'id', 'content', 'timestamp', 'sender__username', 'sender__id'
        )

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    objects = MessageManager()
    unread = UnreadMessagesManager()

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['parent_message']),
            models.Index(fields=['sender', 'receiver']),
        ]

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content[:20]}"

    def mark_as_read(self):
        """Mark message as read if it hasn't been read yet"""
        if not self.read:
            self.read = True
            self.save()
            # Mark related notifications as read
            self.notifications.update(read=True)

    def get_thread(self, depth=0, max_depth=10):
        """Recursively fetch all replies with optimized queries"""
        if depth >= max_depth:
            return []
        
        replies = self.replies.select_related('sender', 'receiver').prefetch_related(
            models.Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver')))
        
        return [{
            'message': reply,
            'replies': reply.get_thread(depth+1, max_depth)
        } for reply in replies]

#notifications linking it to the user and message models

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} regarding message from {self.message.sender.username}'
    
    class Meta:
        ordering = ['-timestamp']
        unique_together = ('user', 'message')

#message history to track edits
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, related_name='edited_messages', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'History for {self.message.id}'

    class Meta:
        ordering = ['-edited_at']


    