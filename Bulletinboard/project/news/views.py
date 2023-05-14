from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

from .filters import PostFilter, ReplyFilter
from .forms import PostForm, MyActivationCodeForm, CreatePostForm, ReplyForm
from .models import *
#from .tasks import notify_users
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.core.cache import cache  # импортируем наш кэш
from django.shortcuts import redirect

import pytz  # импортируем стандартный модуль для работы с часовыми поясами


class Postlist(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    #aginate_by = 10  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ReplyList(ListView):
    model = Reply
    ordering = '-time_in'
    template_name = 'replys.html'
    context_object_name = 'replys'
    #paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        #print(self.request.user)
        if self.request.user.is_authenticated:
            queryset = super().get_queryset().filter(post__author=self.request.user)
        else:
            queryset = super().get_queryset()
        self.filterset = ReplyFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post1'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует так же. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        po = get_object_or_404(Post, id=self.kwargs['pk'])
        context['canedit'] = po.author.username == self.request.user.username
        replys = Reply.objects.filter(post__pk=self.kwargs['pk'])
        context['replys'] = replys
        return context


# Добавляем новое представление для создания .
class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = CreatePostForm
    model = Post
    template_name = 'postcreate.html'

    def form_valid(self, form):
        post1 = form.save(commit=False)
        post1.author = self.request.user
        post1.save()
        # notify_users.apply_async([post1.pk], countdown=5)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['canedit'] = True
        return context


class ReplyCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_reply',)
    form_class = ReplyForm
    model = Reply
    template_name = 'replycreate.html'

    def form_valid(self, form):
        reply1 = form.save(commit=False)
        reply1.user = self.request.user
        po = get_object_or_404(Post, id=self.kwargs['pk'])
        reply1.post = po
        reply1.save()

        user_email = []
        user_email.append(reply1.post.author.email)
        html_content = render_to_string(
            "reply_created_email.html",
            {
                'text': reply1.comment_text,
                'link': f'{settings.SITE_URL}/news/{reply1.post.pk}',
            }
        )
        msg = EmailMultiAlternatives(
            subject='Доска объявлений',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_email
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        # notify_users.apply_async([post1.pk], countdown=5)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['canedit'] = True
        return context


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        po = get_object_or_404(Post, id=self.kwargs['pk'])
        context['canedit'] = po.author == self.request.user
        context['post'] = po
        return context


class ReplyUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_reply',)
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ro = get_object_or_404(Reply, id=self.kwargs['pk'])
        context['canedit'] = ro.user == self.request.user
        context['post'] = ro.post
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        po = get_object_or_404(Post, id=self.kwargs['pk'])
        if not po.author == self.request.user:
            error = "это объявление другого пользователя"
        elif Reply.objects.filter(user = po.author):
            error = 'есть записи откликов по этому объявлению'
        else:
            error = ""
        context['canedit'] = not error == ""
        context['error'] = error
        return context

class ReplyDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_reply',)
    model = Reply
    template_name = 'reply_delete.html'
    success_url = reverse_lazy('reply_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ro = get_object_or_404(Reply, id=self.kwargs['pk'])
        context['canedit'] = ro.post.author == self.request.user
        context['post'] = ro.post
        return context

def endreg(request):
    if request.method == 'POST':
        # user = request.user
        form = MyActivationCodeForm(request.POST)
        if form.is_valid():
            code_use = form.cleaned_data.get("code")
            if Profile.objects.filter(sendedcode=code_use):
                profile = Profile.objects.get(sendedcode=code_use)
            else:
                form.add_error(None, "Код подтверждения не совпадает.")
                return render(request, 'activation_code_form.html', {'form': form})
            if profile.sendedcode == code_use:
                profile.recivedcode = code_use
                profile.save()
                user = profile.user
                if Group.objects.filter(name='authors'):
                    premium_group = Group.objects.get(name='authors')
                    if not user.groups.filter(name='authors').exists():
                        premium_group.user_set.add(user)
                return redirect('/')
            else:
                form.add_error(None, 'Unknown or disabled account')
                return render(request, 'activation_code_form.html', {'form': form})
        else:
            return render(request, 'activation_code_form.html', {'form': form})
    else:
        form = MyActivationCodeForm()
        return render(request, 'activation_code_form.html', {'form': form})

@login_required
def accept(request, pk):
    reply1 = Reply.objects.get(pk=pk)
    user_email = []
    user_email.append(reply1.user.email)
    html_content = render_to_string(
        "reply_accepted_email.html",
        {
            'text': reply1.comment_text,
            'link': f'{settings.SITE_URL}/news/{reply1.post.pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject='Доска объявлений',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=user_email
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    success_url = reverse_lazy('reply_list')
    #return redirect(success_url)
    return render(request, "reply_accepted_email.html")
