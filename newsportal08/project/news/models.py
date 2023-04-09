from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Min, Max, Sum
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.core.cache import cache

article = 'A'
news = 'N'

POSITIONS = [
    (article, 'Статья'),
    (news, 'Новость')
]

# Create your models here.
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True, default=0)

    def update_rating(self):
        total=0

        p = Post.objects.filter(author = self).values("rating", "pk")
        for p1 in p:
            total += 3*p1["rating"]
            c = Comment.objects.filter(post__pk=p1["pk"]).values("rating")
            for c1 in c:
                total += c1["rating"]
        c = Comment.objects.filter(user__pk=self.user.pk).values("rating")
        for c1 in c:
            total += c1["rating"]

        self.rating=total
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')
    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice_field = models.CharField(max_length=1, choices=POSITIONS, default=article)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    article_text = models.TextField()
    rating = models.IntegerField(blank=True, default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.article_text[0:123] + "..."

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    #def __str__(self):
    #    return f'{self.header}: {self.article_text}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(blank=True, default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
