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
    verbose_name_plural = "employee"


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ImagesInline]


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


admin.site.register(Post, PostAdmin)

# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#extending-the-existing-user-model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
