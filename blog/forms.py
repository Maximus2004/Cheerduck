from django import forms

from .models import Post
from .models import Consultation

from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=254, help_text='Это поле обязательно')
  clas = forms.CharField(max_length=2)

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'clas')

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

# class LoginFormView(FormView):
#     form_class = AuthenticationForm

#     # Аналогично регистрации, только используем шаблон аутентификации.
#     template_name = "blog/login.html"

#     # В случае успеха перенаправим на главную.
#     success_url = "blog/signup.html"

#     def form_valid(self, form):
#         # Получаем объект пользователя на основе введённых в форму данных.
#         self.user = form.get_user()
#         self.passw = form.get_password()
#         user = auth.authenticate(self.user, self.passw)
#         if user is not None:
#             return super(LoginFormView, self).form_valid(form)
#         # Выполняем аутентификацию пользователя.
#         login(self.request, self.user)
