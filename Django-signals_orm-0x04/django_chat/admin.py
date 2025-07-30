from django.contrib import admin

# Register your models
from .models import Message, Notification, MessageHistory
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('timestamp',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'read', 'timestamp')
    search_fields = ('user__username', 'message__sender__username')
    list_filter = ('read', 'timestamp')
    ordering = ('-timestamp',)

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'edited_at')
    search_fields = ('message__sender__username', 'message__receiver__username')
    list_filter = ('edited_at',)
    ordering = ('-edited_at',)
