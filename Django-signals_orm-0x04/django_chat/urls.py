from django.urls import path
from . import views

urlpatterns = [
    path('', views.threaded_conversations, name='conversations'),
]