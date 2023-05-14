from django_filters import FilterSet
from .models import Post, Reply

class PostFilter(FilterSet):
    class Meta:
       model = Post
       fields = {
           # поиск по названию
           'header': ['icontains'],
           'author__username': ['icontains'],
           'category__name': ['icontains'],
       }

class ReplyFilter(FilterSet):
    class Meta:
       model = Reply
       fields = {
           # поиск по названию
           'post__article_text': ['icontains'],
           'post__category__name': ['icontains'],
       }