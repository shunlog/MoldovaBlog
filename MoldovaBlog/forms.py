#!/usr/bin/env python3
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .utils import send_verification_email

class UserEmailCreationForm(UserCreationForm):
    '''Override UserCreationForm to add an email field.'''
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = ""
        email = self.cleaned_data["email"]
        send_verification_email(user, email)
        if commit:
            user.save()
        return user

    def clean_email(self):
        '''Verify that the email is unique.
        This is the best place to do it, see https://docs.djangoproject.com/en/5.0/ref/forms/validation/#form-and-field-validation.
        '''
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already used.")
        return data
