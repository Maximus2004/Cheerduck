from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser,PermissionsMixin, User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from typing import Set
from django.contrib import admin, auth 
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import Sum

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
    # email = models.EmailField(default=UserModel.form, editable=False)
    theme = models.TextField("Общая тема лекции-консультации")  # ограниченый размер переменной
    discription = models.TextField("Подробное раскрытие темы") 
    spectators = models.TextField("Целевая аудитория") 
    longliness = models.DurationField("Продолжительность в формате HH:MM:SS") #формат "DD HH:MM:SS

    def publish(self):
        self.creation = timezone.now()
        self.save()

    def __str__(self):
        return self.theme
 
 
class LikeDislikeManager(models.Manager):
    use_for_related_fields = True
 
    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(vote__gt=0)
 
    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(vote__lt=0)
 
    def sum_rating(self):
        # Забираем суммарный рейтинг
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0
    
    def articles(self):
        return self.get_queryset().filter(content_type__model='article').order_by('-articles__pub_date')
 
    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__pub_date')

class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
 
    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )
 
    vote = models.SmallIntegerField(verbose_name=("Голос"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name=("Пользователь"), on_delete=models.PROTECT)
 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
 
    objects = LikeDislikeManager()


class Article(models.Model):
    votes = GenericRelation(LikeDislike, related_query_name='articles')
 
 
class Comment(models.Model):
    votes = GenericRelation(LikeDislike, related_query_name='comments')