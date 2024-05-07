from task_manager.users.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
                'first_name',
                'last_name',
                'username',
                'password1',
                'password2'
                ]
