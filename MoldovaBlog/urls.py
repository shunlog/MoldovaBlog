from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from .views import SignUpView, verify_email, email_form_view

urlpatterns = [
    path("blog/", include("blog.urls")),
    path("admin/", admin.site.urls),

    path("accounts/verify", email_form_view, name="email_form"),
    path("accounts/verify/<token>", verify_email, name="email_verify"),
    path("accounts/signup", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
