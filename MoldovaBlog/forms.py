from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .utils import send_verification_email

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
        if email != "" and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used.")
        return email
