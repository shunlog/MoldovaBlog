from django.contrib import admin

from .models import Post, Comment, Image


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ImagesInline(admin.TabularInline):
    model = Image
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ImagesInline]


admin.site.register(Post, PostAdmin)
