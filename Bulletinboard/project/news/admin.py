from django.contrib import admin
from .models import Category, Post
from modeltranslation.admin import TranslationAdmin

class CategoryAdmin(TranslationAdmin):
    model = Category

# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с новостями
    list_display = [field.name for field in Post._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения
    #list_display.remove('category')
    #list_display.remove('postcategory')
    list_display.remove('reply')
    #print(list_display)
    #list_display = ['id', 'author', 'time_in', 'header', 'article_text', 'rating']
    list_filter = ('author', 'header') # добавляем примитивные фильтры в нашу админку
    search_fields = ('header',) # тут всё очень похоже на фильтры из запросов в базу

admin.site.register(Category)
admin.site.register(Post, PostAdmin)
#admin.site.unregister(Post)