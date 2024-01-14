from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render

from .models import Post, Comment


def index(request):
    return render(request, "blog/index.html")


class PostDetailView(generic.DetailView):
    model = Post


class PostListView(generic.ListView):
    queryset = Post.objects.order_by("-pub_date")
