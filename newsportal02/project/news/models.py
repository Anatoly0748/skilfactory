from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Min, Max, Sum
from django.core.validators import MinValueValidator


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

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


article = 'A'
news = 'N'

POSITIONS = [
    (article, 'Статья'),
    (news, 'Новость')
]

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
