from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from home.models import CustomUser

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'password1', 'password2']