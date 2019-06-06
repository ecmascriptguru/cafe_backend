from django.urls import path, include
from . import views


app_name = 'cafe_backend.settings.emoticons'

urlpatterns = [
    path(
        '', views.EmojiListView.as_view(), name='emoticon_listview'),
    path(
        'new', views.EmoticonCreateView.as_view(), name='emoticon_createview'),
    path(
        '<int:pk>/edit', views.EmoticonUpdateView.as_view(),
        name='emoticon_updateview'),
    path(
        '<int:pk>/delete', views.EmoticonDeleteView.as_view(),
        name='emoticon_deleteview'),
]
