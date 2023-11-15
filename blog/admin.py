from django.contrib import admin
from django.contrib import admin
from .models import Post, News as New, User

# регистрация модели поста
admin.site.register(Post)
admin.site.register(New)
admin.site.register(User)

# Register your models here.
