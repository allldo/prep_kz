from django.contrib import admin
from django.urls import path
from .views import main_forum, topic, create_topic
app_name = 'forum'

urlpatterns = [
    path('', main_forum, name='forum_main'),
    path('topic/<int:topic_id>', topic, name='topic'),
    path('topic/create_topic/<str:topic_name>', create_topic, name='create_topic'),
]
