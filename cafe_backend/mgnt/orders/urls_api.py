from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from cafe_backend.apps.dishes.views import DishReviewViewSet
from . import views


router = DefaultRouter()
router.register('orders', views.OrderViewSet)

order_router = routers.NestedSimpleRouter(
    router, r'orders', lookup='order')
order_router.register(r'items', views.OrderItemViewSet, base_name='items')

order_item_router = routers.NestedSimpleRouter(
    order_router, r'items', lookup='order_item')
order_item_router.register(
    r'reviews', DishReviewViewSet, base_name='reviews')

router.register('items', views.OrderItemViewSet)
item_router = routers.NestedDefaultRouter(
    router, r'items', lookup='order_item')
item_router.register(r'reviews', DishReviewViewSet, base_name='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(order_router.urls)),
    path('', include(order_item_router.urls)),
    path('', include(item_router.urls)),
]
