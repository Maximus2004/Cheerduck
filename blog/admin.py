from django.contrib import admin
from .models import Post, Consultation, UserModel

admin.site.register(Post)
admin.site.register(Consultation)
admin.site.register(UserModel)