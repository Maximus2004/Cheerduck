from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    # создаём поля для объекта модели поста, который будет находится в бд
    title = models.CharField("Тема консультации", max_length=200)  # ограниченый размер переменной
    text = models.TextField("Раскрытие темы")  # текст для поста
    published_date = models.DateTimeField(blank=True, null=True, default=timezone.now)  # дата
    good_date = models.DateTimeField("Удобная дата проведения", default=timezone.now)  # удобная дата проведения
    likes = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class UserModel(AbstractUser):
    form = models.CharField(max_length=2)
    vk = models.CharField(max_length=200, blank=True, null=True)
    # grades = models.IntegerField(default=0)
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class Consultation(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")
    creation = models.DateTimeField(default=timezone.now, editable=False)
    date = models.DateTimeField("Дата проведения лекции-консультации", default=timezone.now)
    email = models.EmailField("Ваша почта", default="")  # предназначен для ввода адреса электронной почты
    theme = models.TextField("Общая тема лекции-консультации", default="")
    discription = models.TextField("Подробное раскрытие темы", default="")
    spectators = models.TextField("Целевая аудитория", default="")
    longliness = models.CharField('Продолжительность консультации', max_length=20, default="")
    members = models.ManyToManyField(UserModel, related_name='+')  # участники консультации
    posts = models.ForeignKey(Post, on_delete=models.CASCADE, default="", blank=True, null=True)
    contact = models.IntegerField('Форма взаимодействия', choices=[(1, "Очно"), (2, "Заочно")], default="")
    place = models.CharField('Место проведения', max_length=20, default="")
    hashteg = models.CharField('Место проведения', max_length=200, default="")
    hashtegs = []

    def publish(self):
        self.creation = timezone.now()
        self.save()

    def __str__(self):
        return self.theme