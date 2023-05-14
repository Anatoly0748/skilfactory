from django.db.models.signals import m2m_changed
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import Reply

def send_notification(text, pk, subject, to):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': text,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@receiver(m2m_changed, sender=Reply)
def notify_about_new_reply(sender, reply, **kwargs):
    print( kwargs['action'])
    if kwargs['action'] == 'reply_add':
        user_email = []
        user_email.append(reply.post.author.email)
        html_content = render_to_string(
            "reply_created_email.html",
            {
                'text': reply.comment_text,
                'link': f'{settings.SITE_URL}/news/{reply.post.id}',
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
