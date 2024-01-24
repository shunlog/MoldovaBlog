from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

from .utils import send_verification_email


def verify_unique_email(email):
    if email != "" and User.objects.filter(email=email).exists():
        raise forms.ValidationError("This email is already used.")


class UserEmailCreationForm(UserCreationForm):
    '''Override UserCreationForm to add an email field.'''
    email = forms.EmailField(label='Email', required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def send_verification_email(self):
        # example: https://docs.djangoproject.com/en/5.0/topics/class-based-views/generic-editing/#basic-forms
        email = self.cleaned_data["email"]
        username = self.cleaned_data["username"]
        send_verification_email(username, email)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = ""
        if commit:
            user.save()
        return user

    def clean_email(self):
        '''Verify that the email is unique.
        This is the best place to do it, see https://docs.djangoproject.com/en/5.0/ref/forms/validation/#form-and-field-validation.
        '''
        email = self.cleaned_data['email']
        verify_unique_email(email)
        return email


class EmailForm(LoginRequiredMixin, forms.Form):
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))

    def __init__(self, request=None, *args, **kwargs):
        """ The 'request' parameter is needed for getting the username"""
        self.request = request
        super().__init__(*args, **kwargs)

    def clean_password(self):
        self.cleaned_data['username'] = self.request.user.username
        # this form will raise errors if (username, password) aren't correct
        f = AuthenticationForm(self.request, self.cleaned_data)
        if not f.is_valid():
            raise ValidationError("Please enter a correct password", code="incorrect")
        return self.cleaned_data['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        verify_unique_email(email)
        return email

    def send_verification_email(self):
        email = self.cleaned_data["email"]
        username = self.request.user.username
        send_verification_email(username, email)
