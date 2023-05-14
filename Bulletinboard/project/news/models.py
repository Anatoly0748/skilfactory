from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Min, Max, Sum
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.core.cache import cache
from djrichtextfield.models import RichTextField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sendedcode = models.CharField(max_length=50,blank=True, null=True, default=None)
    recivedcode = models.CharField(max_length=50, blank=True, null=True, default=None)

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    article_text = models.TextField()

    def preview(self):
        return self.article_text[0:123] + "..."

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        #return self.article_text
        return f'{self.author.username}: {self.header}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post.pk)])
