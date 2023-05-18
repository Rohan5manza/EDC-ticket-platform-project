from django import forms
from .models import Ticket
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class UserRegistrationForm(UserCreationForm):
    #adds a new 'email' field to the form, which is required
    email=forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class FreeTicketForm(forms.Form):
    email= forms.EmailField()

class BuyTicketForm(forms.Form):
    name= forms.CharField()
    email=forms.EmailField()

class TicketForm(forms.ModelForm):
    class Meta:
        model=Ticket
        fields=['name','email']        