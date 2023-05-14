from djrichtextfield.widgets import RichTextWidget
from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Reply

class PostForm(forms.ModelForm):
    article_text = forms.CharField(widget=RichTextWidget())

    class Meta:
       model = Post
       fields = ['category', 'header', 'article_text', ]

    def clean(self):
       cleaned_data = super().clean()
       name = cleaned_data.get("name")
       description = cleaned_data.get("description")

       #if vname == description:
       #    raise ValidationError(
       #        "Описание не должно быть идентично названию."
       #    )

       return cleaned_data

class CreatePostForm(forms.ModelForm):
    article_text = forms.CharField(widget=RichTextWidget())
    class Meta:
       model = Post
       fields = ['category', 'header', 'article_text', ]

class ReplyForm(forms.ModelForm):
    class Meta:
       model = Reply
       fields = ['comment_text', ]

class MyActivationCodeForm(forms.Form):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз."),
                      'password_mismatch':
                          ("Пароли не совпадают."),
                      'cod-no':
                          ("Код не совпадает."),}


    def __init__(self, *args, **kwargs):
        super(MyActivationCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True, max_length=50, label='Код подтвержения',
                           widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                           error_messages={'required': 'Введите код!','max_length': 'Максимальное количество символов 50'})



    def save(self, commit=True):
        profile = super(MyActivationCodeForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']

        if commit:
            profile.save()
        return profile