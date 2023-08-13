
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post,Image
from django.forms import ModelForm



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserLoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1']

class Create_PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content']

class Update_post(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class UserPicUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']

        