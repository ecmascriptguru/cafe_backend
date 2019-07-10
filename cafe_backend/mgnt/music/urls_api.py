from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = DefaultRouter()
router.register('music', views.MusicViewSet)
router.register('playlist', views.PlaylistViewSet)

# channel_router = routers.NestedSimpleRouter(
#     router, r'channels', lookup='channel')
# channel_router.register(
# r'items', views.ChannelItemViewSet, base_name='items')


urlpatterns = [
    # path(
    #     'music/search/', views.MusicSearchAPIView.as_view(),
    #     name='music_search_api'),

    path('', include(router.urls)),
]
