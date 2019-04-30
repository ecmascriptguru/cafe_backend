from django.urls import path, include
from . import views


app_name = 'cafe_backend.apps.dishes'

urlpatterns = [
    path(
        'categories/', views.CategoryListView.as_view(),
        name='category_listview'),
    path(
        'categories/<int:pk>', views.CategoryUpdateView.as_view(),
        name='category_updateview'),

    path('dishes/', views.DishListView.as_view(), name='dish_listview'),
]
