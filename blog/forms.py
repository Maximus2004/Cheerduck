from django import forms

from .models import Post
from .models import User
from .models import Consultation


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class UserForm(forms.ModelForm):

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput)
        model = User
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ('username', 'surname', 'email', 'password', 'clas')

class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation
        fields = ('creation', 'date', 'email', 'theme', 'discription', 'spectators', 'longliness')