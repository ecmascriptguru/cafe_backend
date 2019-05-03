from django.urls import path, include
from . import views


app_name = 'cafe_backend.apps.dishes'

urlpatterns = [
    path(
        'categories/', views.CategoryListView.as_view(),
        name='category_listview'),
    path(
        'categories/new', views.CategoryCreateView.as_view(),
        name='category_createview'),
    path(
        'categories/<int:pk>', views.CategoryUpdateView.as_view(),
        name='category_updateview'),

    path('dishes/', views.DishListView.as_view(), name='dish_listview'),
    path(
        'dishes/new', views.DishCreateView.as_view(),
        name='dish_createview'),
    path(
        'dishes/<int:pk>', views.DishUpdateView.as_view(),
        name='dish_updateview'),
]
