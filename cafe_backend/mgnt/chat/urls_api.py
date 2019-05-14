from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = DefaultRouter()
router.register('channels', views.ChannelViewSet)

# channel_router = routers.NestedSimpleRouter(
#     router, r'channels', lookup='channel')
# channel_router.register(
# r'items', views.ChannelItemViewSet, base_name='items')


urlpatterns = [
    path('', include(router.urls)),
    # path('', include(order_router.urls)),
]
