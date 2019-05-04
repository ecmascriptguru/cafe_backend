from django.views import generic
from django.db.models import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db import transaction
from rest_framework import viewsets, permissions
from .serializers import CategorySerializer, DishSerializer, ReviewSerializer
from . import forms
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

    def get_queryset(self, **kwargs):
        if self.kwargs.get('category_pk'):
            return self.queryset.filter(
                category_id=self.kwargs.get('category_pk'))
        else:
            return self.queryset


class DishReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = ReviewSerializer
    queryset = DishReview.objects.all()

    def perform_create(self, serializer):
        serializer.save(dish_id=self.kwargs.get('dish_pk'))
        return super().perform_create(serializer)

    def get_queryset(self, **kwargs):
        if self.kwargs.get('dish_pk'):
            return self.queryset.filter(
                dish_id=self.kwargs.get('dish_pk'))
        else:
            return self.queryset


class CategoryListView(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'categories/category_listview.html'


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    template_name = 'categories/category_updateview.html'
    form_class = forms.CategoryForm


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    template_name = 'categories/category_createview.html'
    form_class = forms.CategoryForm


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = 'dishes/dish_listview.html'


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = forms.DishForm
    template_name = 'dishes/dish_createview.html'
    success_url = None

    def get_context_data(self, *args, **kwargs):
        data = super(DishCreateView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            data['images'] = forms.DishImageFormSet(self.request.POST)
        else:
            data['images'] = forms.DishImageFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        with transaction.atomic():
            self.object = form.save()
            if images.is_valid():
                images.instance = self.object
                images.save()
        return super(DishCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dishes:dish_listview')


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = forms.DishForm
    template_name = 'dishes/dish_updateview.html'
    success_url = None

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        with transaction.atomic():
            self.object = form.save()
            if images.is_valid():
                images.instance = self.object
                images.save()
        return super(DishUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('dishes:dish_listview')

    def get_context_data(self, *args, **kwargs):
        data = super(DishUpdateView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            data['images'] = forms.DishImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['images'] = forms.DishImageFormSet(instance=self.object)
        return data
