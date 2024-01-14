from django.http import HttpResponse
from django.views import generic

from .models import Post, Comment


def index(request):
    return HttpResponse("Hello, world. You're at the blog index.")


class PostDetailView(generic.DetailView):
    model = Post


class PostListView(generic.ListView):
    queryset = Post.objects.order_by("-pub_date")
