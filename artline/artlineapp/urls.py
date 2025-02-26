from django.urls import path
from .views import home, video_feed

urlpatterns = [
    path('', home, name='home'),
    path('video_feed/', video_feed, name='video_feed'),
]