from models import Post, Category

category = Category.objects.get(name="Тема4")
p = Post.objects.filter(category == category)