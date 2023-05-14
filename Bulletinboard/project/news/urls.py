from django.urls import path
# Импортируем созданное нами представление
from .views import Postlist, PostDetail, PostCreate, PostUpdate, PostDelete
from .views import endreg, ReplyList, ReplyCreate, ReplyUpdate, ReplyDelete, accept
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('',  Postlist.as_view(), name='post_list'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('activation_code_form/', endreg, name="endreg"),
   path('reply/', ReplyList.as_view(), name='reply_list'),
   path('<int:pk>/replycreate/', ReplyCreate.as_view(), name='reply_create'),
   path('<int:pk>/replyedit/', ReplyUpdate.as_view(), name='reply_edit'),
   path('<int:pk>/replydelete/', ReplyDelete.as_view(), name='reply_delete'),
   path('<int:pk>/accept/', accept, name="accept"),
]