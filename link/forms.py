from django import forms
from .models import Application
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['name', 'photo', 'link']

