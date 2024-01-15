#!/usr/bin/env python3
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserEmailCreationForm(UserCreationForm):
    '''Override UserCreationForm to add an email field.'''
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def clean_email(self):
        # https://docs.djangoproject.com/en/5.0/ref/forms/validation/#form-and-field-validation
        data = self.cleaned_data['email']
        # TODO check if the user is in the "email_verified" group instead
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already used.")
        return data
