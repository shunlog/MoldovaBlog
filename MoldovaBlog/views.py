from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import UserEmailCreationForm, EmailForm
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


@login_required
def email_form_view(request):
    success_url = reverse_lazy("blog:index")
    template_name = "registration/add_email.html"

    def form_valid(form):
        form.send_verification_email()

    if request.method == "POST":
        form = EmailForm(request, request.POST)
        if form.is_valid():
            form_valid(form)
            return HttpResponseRedirect(success_url)

    else:
        form = EmailForm()

    return render(request, template_name, {"form": form})



# class EmailFormView(LoginRequiredMixin, generic.FormView):
#     form_class = EmailForm
#     template_name = "registration/add_email.html"
#     success_url = reverse_lazy("blog:index")

#     def form_valid(self, form):
#         form.send_verification_email(self.request.user)
#         return super().form_valid(form)
