from django import forms
from .models import CustomUser, Account
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'

