from django.views import generic
from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets, permissions
from .serializers import CategorySerializer, DishSerializer, ReviewSerializer
from .forms import CategoryForm
from .models import Category, Dish, DishReview


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True)


class DishViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = DishSerializer
    queryset = Dish.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(category_id=self.kwargs.get('category_pk'))
        return super().perform_create(serializer)


class DishReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = ReviewSerializer
    queryset = DishReview.objects.all()

    def perform_create(self, serializer):
        serializer.save(dish_id=self.kwargs.get('dish_pk'))
        return super().perform_create(serializer)


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
