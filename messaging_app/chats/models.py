from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    display_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username
    
class Conversation(models.Model):
    """
    Model representing a conversation between users.
    """
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} with {self.participants.count()} participants"
    
class Message(models.Model):
    """
    Model representing a message in a conversation.
    """
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username} in Conversation {self.conversation.id}"
