from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    # создаём поля для объекта модели поста, который будет находится в бд
    #author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # ссылка на другую модель
    title = models.CharField(max_length=200) # ограниченый размер переменной
    text = models.TextField() # текст для поста
    created_date = models.DateTimeField(default=timezone.now) # дата
    published_date = models.DateTimeField(blank=True, null=True) # дата

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title