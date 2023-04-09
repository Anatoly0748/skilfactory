from django.urls import path
# Импортируем созданное нами представление
from .views import Postlist, PostDetail, PostCreate, PostUpdate, PostDelete, subscribe
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('',  cache_page(60)(Postlist.as_view()), name='post_list'),
   path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/subscribe/', subscribe, name='subscribe'),
]