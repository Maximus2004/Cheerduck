from django.conf import settings
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser,PermissionsMixin


class Post(models.Model):
    # создаём поля для объекта модели поста, который будет находится в бд
    title = models.CharField("Тема консультации", max_length=200) # ограниченый размер переменной
    text = models.TextField("Раскрытие темы") # текст для поста
    published_date = models.DateTimeField(blank=True, null=True) # дата

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class UserModel(AbstractUser):
    form = models.CharField(max_length=2)
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

class Consultation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creation = models.DateTimeField(default=timezone.now, editable=False) 
    date = models.DateTimeField("Дата проведения лекции-консультации", default=timezone.now) 
    email = models.EmailField("Ваша почта") #предназначен для ввода адреса электронной почты и создает следующую разметку:
    # email = models.EmailField(default=UserModel.form, editable=False) #предназначен для ввода адреса электронной почты и создает следующую разметку:
    theme = models.TextField("Общая тема лекции-консультации")  # ограниченый размер переменной
    discription = models.TextField("Подробное раскрытие темы") 
    spectators = models.TextField("Целевая аудитория") 
    longliness = models.DurationField("Продолжительность в формате HH:MM:SS") #формат "DD HH:MM:SS

    def publish(self):
        self.creation = timezone.now()
        self.save()

    def __str__(self):
        return self.theme