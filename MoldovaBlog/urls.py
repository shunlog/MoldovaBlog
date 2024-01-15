from django.contrib import admin
from django.urls import include, path

from .views import SignUpView, verify_email

urlpatterns = [
    path("blog/", include("blog.urls")),
    path("admin/", admin.site.urls),

    path("accounts/verify/<token>", verify_email, name="email_verify"),
    path("accounts/signup", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
]
