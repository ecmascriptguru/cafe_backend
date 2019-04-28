from django.views import generic
from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets
from .serializers import CategorySerializer
from .forms import CategoryForm
from .models import Category, Dish


class CategoryViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'categories/category_listview.html'


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    template_name = 'categories/category_updateview.html'
    form_class = CategoryForm


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = 'dishes/dish_listview.html'
