from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Post, Comment, Image, Profile


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ImagesInline(admin.TabularInline):
    model = Image
    extra = 0


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ImagesInline]
    list_display = ["title", "author", "pub_date"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["text", "author", "pub_date"]


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = list(BaseUserAdmin.list_display) + ["date_joined"]


class ImageAdmin(admin.ModelAdmin):
    list_display = ["file", "post", "alt"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image, ImageAdmin)

# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#extending-the-existing-user-model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
