from django.contrib import admin
from django.urls import path
from .views import main_forum, topic, create_post, new_post, post_detail,\
    like, dislike, new_comment, submit_report, delete_content
app_name = 'forum'

urlpatterns = [
    path('', main_forum, name='forum_main'),
    path('topic/<int:topic_id>', topic, name='topic'),
    path('topic/create_post/<str:topic_name>', create_post, name='create_post'),
    path('topic/<str:topic_name>/new_post', new_post, name='new_post'),
    path('topic/<str:post_name>/new_comment', new_comment, name='new_comment'),
    path('topic/post_detail/<int:post_id>', post_detail, name='post_detail'),

    path('forum/post_detail/<int:post_id>/like', like, name='like'),
    path('forum/post_detail/<int:post_id>/dislike', dislike, name='dislike'),

    path('forum/post_detail/<int:post_id>/submit_report', submit_report, name='submit_report'),
    path('forum/post_detail/<int:post_id>/delete_content', delete_content, name='delete_content'),

    # path('forum/user/<int:user_id>/ban', ban_user, name='ban_user'),

]
