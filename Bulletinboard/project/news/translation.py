from .models import Category
from modeltranslation.translator import register,  TranslationOptions


# регистрируем наши модели для перевода

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)  # указываем, какие именно поля надо переводить в виде кортежа