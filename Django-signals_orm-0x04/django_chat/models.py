#sender
#receiver
#content
#timestamp

from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return (
            self.get_queryset()
            .filter(receiver=user, read=False) 
            .only('id', 'sender', 'receiver', 'content', 'timestamp')
            .select_related('sender', 'receiver')
        )
        

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)

    parent_message = models.ForeignKey(
        'self', null=True, blank=True,
        related_name='replies', on_delete=models.CASCADE
    )

    objects = models.Manager()
    unread = UnreadMessagesManager() 

    def __str__(self):
        return f'Message from {self.sender.username} to {self.receiver.username} at {self.timestamp}'

    class Meta:
        ordering = ['-timestamp']
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

    def __str__(self):
        return f'History for {self.message.id}'

    class Meta:
        ordering = ['-edited_at']


    