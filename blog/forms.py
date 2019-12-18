from django import forms

from .models import Post
from .models import Consultation

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=254, help_text='Это поле обязательно')
  Class = forms.CharField(max_length=2, help_text='Впишите сюда класс, в котором вы обучаетесь')

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'Class')

class RegisterFormView(FormView):
    form_class = SignUpForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "blog/new_user.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email')

class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation
        fields = ('creation', 'date', 'email', 'theme', 'discription', 'spectators', 'longliness')
