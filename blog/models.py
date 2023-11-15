from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission


class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='users')
    user_permissions = models.ManyToManyField(Permission, related_name='users_permissions')


class Post(models.Model):
    title = models.CharField(max_length=450)
    body = models.TextField()
    img = models.TextField(null=True)
    country = models.CharField(max_length=250)
    author = models.ForeignKey(
        'blog.User',
        on_delete=models.CASCADE,
    )

    # метод
    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=450)
    body = models.TextField(null=True)
    image = models.URLField(null=True, default=None)
    time = models.DateTimeField(null=True)

    # метод
    def __str__(self):
        return self.title


