from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views


router = DefaultRouter()
router.register('bookings', views.BookingViewSet)

booking_router = routers.NestedSimpleRouter(
    router, r'bookings', lookup='booking')
booking_router.register(
    r'messages', views.BookingMessageViewSet, base_name='messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(booking_router.urls)),
]
