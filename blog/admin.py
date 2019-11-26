from django.contrib import admin
from .models import Post
from .models import User

admin.site.register(Post)
admin.site.register(User)