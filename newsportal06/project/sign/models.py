from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",

                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        #user.save()
        user_email = []
        user_email.append(user.email)
        html_content = render_to_string(
            'sign/user_created_email.html',
            {

                }
        )
        msg = EmailMultiAlternatives(
            subject='News Portal',
            body='Поздравляем вас с успешной регистрацией на сайте News Portal',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_email
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        return user