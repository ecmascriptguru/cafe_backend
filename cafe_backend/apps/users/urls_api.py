from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = DefaultRouter()
router.register('tables', views.TableViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
