from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = DefaultRouter()
router.register('emoticons', views.EmoticonViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
