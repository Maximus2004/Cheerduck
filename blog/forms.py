from django import forms

from .models import Post, Consultation

from django.contrib.auth.forms import UserCreationForm
from .models import UserModel


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'good_date',)


class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation
        fields = ('date', 'theme', 'discription', 'spectators', 'longliness', 'contact', 'place', 'hashteg',)


CHOICES = [(1, 'Очно'), (2, 'Заочно')]


class FilterDate(forms.Form):
    dateFrom = forms.DateTimeField(label="Дата от", required=False)
    dateTo = forms.DateTimeField(label="Дата до", required=False)
    search = forms.CharField(label="Поиск", required=False)
    contact = forms.MultipleChoiceField(label="Форма проведения", choices=CHOICES, required=False)
    hashtegs = forms.CharField(label="Хештеги", required=False)


class SignUp(UserCreationForm):
    form = forms.CharField(max_length=2, help_text='Введите класс, в котором вы обучаетесь')
    # password1 = UserModel.password1
    # password2 = UserModel.password2

    class Meta:
        model = UserModel
        fields = ('form', 'email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'vk',)