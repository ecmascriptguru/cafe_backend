from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Dish


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class DishTranslationOptions(TranslationOptions):
    fields = ('name', 'description', )


translator.register(Category, CategoryTranslationOptions)
translator.register(Dish, DishTranslationOptions)
