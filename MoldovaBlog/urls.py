from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", include("blog.urls")),
    path("admin/", admin.site.urls),

    path("accounts/verify/done", views.email_sent, name="email_sent"),
    path("accounts/verify", views.email_form_view, name="email_form"),
    path("accounts/verify/<token>", views.verify_email, name="email_verify"),
    path("accounts/signup", views.SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
