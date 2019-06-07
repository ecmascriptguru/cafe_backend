from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = DefaultRouter()
router.register('videos', views.VideoViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
