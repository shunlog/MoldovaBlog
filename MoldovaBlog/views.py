from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse

from .forms import UserEmailCreationForm
from .utils import validate_verification_token


class SignUpView(generic.CreateView):
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.forms.BaseUserCreationForm
    # Tutorial: https://learndjango.com/tutorials/django-signup-tutorial
    form_class = UserEmailCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def verify_email(request, token):
    try:
        username, email = validate_verification_token(token)
    except:
        return HttpResponse("Couldn't validate token")

    return HttpResponse(f"{username}, your email has been verified: {email}")
