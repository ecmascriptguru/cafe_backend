from django.urls import path, include
from . import views


app_name = 'cafe_backend.settings.videos'

urlpatterns = [
    path(
        '', views.VideoListView.as_view(), name='video_listview'),
    path(
        'new', views.VideoCreateView.as_view(), name='video_createview'),
    path(
        '<int:pk>/', views.VideoDetailView.as_view(),
        name='video_detailview'),
    path(
        '<int:pk>/edit', views.VideoUpdateView.as_view(),
        name='video_updateview'),
    path(
        '<int:pk>/delete', views.VideoDeleteView.as_view(),
        name='video_deleteview'),
]
