from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200)
    def __str__(self):
        return self.category_name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = CloudinaryField('image', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
