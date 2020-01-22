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
        fields = ('title', 'text',)

# class UserForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = ('username', 'email')

class ConsultationForm(forms.ModelForm):        

    class Meta:
        model = Consultation
        fields = ('date', 'theme', 'discription', 'spectators', 'longliness',)


class SignUp(UserCreationForm):
    form = forms.CharField(max_length=2, help_text='Введите класс, в котором вы обучаетесь')

    class Meta:
        model = UserModel
        fields = ('form', 'email', 'password1', 'password2', 'username', 'first_name', 'last_name',)

# class SignUpForm(UserCreationForm):
#     # email = forms.EmailField(max_length=254)
#     # Class = forms.CharField(max_length=2)
#     # help_texts = {
#     #     'email': ' ',
#     # } 
#     class Meta:
#         model = UserModel
#         fields = ('user', 'form')

# class RegisterFormView(FormView):
#     form_class = SignUpForm
#     # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
#     # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
#     success_url = '/'

#     # Шаблон, который будет использоваться при отображении представления.
#     template_name = "blog/signup.html"

#     def form_valid(self, form):
#         # Создаём пользователя, если данные в форму были введены корректно.
#         form.save()
#         # Вызываем метод базового класса
#         return super(RegisterFormView, self).form_valid(form)