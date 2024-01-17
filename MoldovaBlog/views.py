from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse

from .forms import UserEmailCreationForm
from .utils import assign_email


class SignUpView(generic.CreateView):
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.forms.BaseUserCreationForm
    # Tutorial: https://learndjango.com/tutorials/django-signup-tutorial
    form_class = UserEmailCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # example: https://docs.djangoproject.com/en/5.0/topics/class-based-views/generic-editing/#basic-forms
        form.send_verification_email()
        return super().form_valid(form)


def verify_email(request, token):
    try:
        username, email = assign_email(token)
    except ValueError as e:
        return HttpResponse(f"Couldn't validate token, {e}", status=400)

    return HttpResponse(f"{username}, your email has been verified: {email}")
