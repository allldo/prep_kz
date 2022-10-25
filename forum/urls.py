from django.contrib import admin
from django.urls import path
from .views import main_forum
app_name = 'forum'

urlpatterns = [
    path('', main_forum, name='forum_main'),
]
