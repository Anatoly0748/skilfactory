import datetime
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category
from celery import app

def send_notification(preview, pk, header, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=header,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def notify_users(id):
    #print(id, "Взят из очереди")
    instance = Post.objects.get(pk = id)
    categories = instance.category.all()
    subscribers_emails = []
    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]
    send_notification(instance.preview(), instance.pk, instance.header, subscribers_emails)

@shared_task
def weekly_news():
    #print("weekly_news")
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject = 'Статьи за неделю',
        body = '',
        from_email = settings.DEFAULT_FROM_EMAIL,
        to = subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
