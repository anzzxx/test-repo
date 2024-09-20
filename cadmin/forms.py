from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.forms import EmailField
from django.contrib.auth.models import User
from django import forms

class Registeruser(UserCreationForm):
    email = EmailField(label="Email Address", required=True)
    class Meta:
        
        
         model = User
         fields = ['username', 'email', 'password1', 'password2', 'is_superuser']

class EditForm(UserChangeForm):
    password=None
    class Meta:
        model=User
        fields=['username','email','is_superuser']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'})
            
        }
        