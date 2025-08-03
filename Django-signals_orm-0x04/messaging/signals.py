#signal to listen for the post_save signal and send notification when a new message instance is created
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification, User


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the receiver of the message
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
        )
        print(f'Notification created for {instance.receiver.username} regarding new message from {instance.sender.username}.')

@receiver(pre_save, sender=Message, dispatch_uid='message_pre_save')
def log_message_history(sender, instance, **kwargs):
    if instance.pk:
        # If the message is being edited, save the old content to history
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
            )
            instance.edited = True 
            print(f'Message {instance.pk} edited. Old content saved to history.')
        except Message.DoesNotExist:
            pass


#signal to clean up related data when a user deletes account
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications related to the user
    Notification.objects.filter(user=instance).delete()
    
    # Delete all message history related to messages sent or received by the user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
    
    print(f'All data related to user {instance.username} has been deleted.')
        
            