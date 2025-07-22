import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sender = django_filters.CharFilter(field_name='sender__username', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = ['sent_after', 'sent_before', 'sender']

        