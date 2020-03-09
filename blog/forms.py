from django import forms

from .models import Post
from .models import Consultation
from .models import UserModel
from django.contrib.auth.models import User

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserModel


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'good_date',)


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ('date', 'theme', 'discription', 'spectators', 'longliness', 'contact', 'place',)


class SignUp(UserCreationForm):
    form = forms.CharField(max_length=2, help_text='Введите класс, в котором вы обучаетесь')
    # vk = forms.CharField(max_length=200, help_text='Введите ссылку на свой аккаунт в ВК', default="")

    class Meta:
        # password = forms.CharField(widget=forms.PasswordInput)
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }
        model = UserModel
        fields = ('form', 'email', 'password1', 'password2', 'username', 'first_name', 'last_name', 'vk',)
