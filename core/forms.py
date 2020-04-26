from django.contrib.auth.forms import UserCreationForm
from django import forms
from core.models import Classroom, ClassPeople
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class CreateClass(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name','subject']
