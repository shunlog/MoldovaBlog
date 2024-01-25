from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.HomePageView.as_view(), name="index"),
    path("about/", views.about, name="about"),
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("user/edit", views.ProfileUpdateView.as_view(), name="profile_update"),
    path("user/<int:pk>", views.UserDetailView.as_view(), name="user_detail"),
    path("<int:post_pk>/comment/", views.create_comment, name="create_comment"),
]
