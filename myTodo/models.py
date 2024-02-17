from django.db import models
from django.contrib.auth.models import User
from datetime import time
# Create your models here.

from django import forms
from django.contrib.auth.forms import UserCreationForm



class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date_complete = models.DateField()
    time = models.TimeField(auto_now=True)
    complete = models.BooleanField(default=False)


    def __str__(self) -> str:
        return self.title
    

    class Meta:
        ordering = ['date_complete','complete']


class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    # name = models.CharField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username



