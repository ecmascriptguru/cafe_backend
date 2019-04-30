from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('dishes', views.DishViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
