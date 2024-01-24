from django.urls import reverse_lazy, reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import UserEmailCreationForm, ChangeEmailForm
from .utils import assign_email, send_verification_email


class SignUpView(generic.CreateView):
    # https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.forms.BaseUserCreationForm
    # Tutorial: https://learndjango.com/tutorials/django-signup-tutorial
    form_class = UserEmailCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        # example: https://docs.djangoproject.com/en/5.0/topics/class-based-views/generic-editing/#basic-forms
        email = form.cleaned_data["email"]
        username = form.cleaned_data["username"]
        hostname = self.request.get_host()
        send_verification_email(hostname, username, email)

        return super().form_valid(form)


def verify_email(request, token):
    try:
        username, email = assign_email(token)
    except ValueError as e:
        return HttpResponse(f"Couldn't validate token, {e}", status=400)

    return render(request, "registration/email_confirmed.html")


def email_sent(request):
    return render(request, "registration/email_sent.html")


@login_required
def email_form_view(request):
    success_url = reverse("email_sent")
    template_name = "registration/add_email.html"

    def form_valid(form):
        username = request.user.username
        email = form.cleaned_data["email"]
        hostname = request.get_host()
        send_verification_email(hostname, username, email)

    if request.method == "POST":
        form = ChangeEmailForm(request, request.POST)
        if form.is_valid():
            form_valid(form)
            return HttpResponseRedirect(success_url)

    else:
        form = ChangeEmailForm()

    return render(request, template_name, {"form": form})
