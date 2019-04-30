from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = DefaultRouter()
router.register('categories', views.CategoryViewSet)

category_router = routers.NestedSimpleRouter(
    router, r'categories', lookup='category')
category_router.register(r'dishes', views.DishViewSet, base_name='dishes')

category_dish_router = routers.NestedSimpleRouter(
    category_router, r'dishes', lookup='dish')
category_dish_router.register(
    r'reviews', views.DishReviewViewSet, base_name='reviews')

router.register('dishes', views.DishViewSet)
dish_router = routers.NestedDefaultRouter(
    router, r'dishes', lookup='dish')
dish_router.register(r'reviews', views.DishReviewViewSet, base_name='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(category_router.urls)),
    path('', include(category_dish_router.urls)),
    path('', include(dish_router.urls)),
]
