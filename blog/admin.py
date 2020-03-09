from django.contrib import admin
from .models import Consultation, UserModel, Post

admin.site.register(Post)
admin.site.register(Consultation)
admin.site.register(UserModel)