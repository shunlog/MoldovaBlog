from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .forms import UserEmailCreationForm


class SignUpView(generic.CreateView):
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.forms.BaseUserCreationForm
    # Tutorial: https://learndjango.com/tutorials/django-signup-tutorial
    form_class = UserEmailCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
