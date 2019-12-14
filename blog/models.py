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

class User(models.Model):
    username = models.CharField("Имя", max_length=50, default='') # ограниченый размер переменной, потому что user не должен быть большим
    surname = models.CharField("Фамилия", max_length=50, default='')
    email = models.EmailField("Ваша почта", default='')
    password = models.TextField("Пароль") 
    clas = models.IntegerField("Класс", default=0)

    def __str__(self):
        return self.username

class Consultation(models.Model):
    creation = models.DateTimeField("Дата создания (редактированию не подлежит)", default=timezone.now) 
    date = models.DateTimeField("Дата проведения лекции-консультации       ", default=timezone.now) 
    email = models.EmailField("Ваша почта                                ") #предназначен для ввода адреса электронной почты и создает следующую разметку:
    theme = models.TextField("Общая тема лекции-консультации             ")  # ограниченый размер переменной
    discription = models.TextField("Подробное раскрытие темы                  ") 
    spectators = models.TextField("Целевая аудитория                         ") 
    longliness = models.DurationField("Продолжительность в формате HH:MM:SS      ") #формат "DD HH:MM:SS

    def publish(self):
        self.creation = timezone.now()
        self.save()


    def __str__(self):
        return self.theme