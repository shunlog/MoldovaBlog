from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.contrib.auth.models import User

from .models import Post, Comment, Profile
from .forms import CommentForm


def index(request):
    return render(request, "blog/index.html")


class UserDetailView(DetailView):
    model = User
    template_name = "blog/profile.html"
    context_object_name = "userobj"  # don't overwrite "user" object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = User.objects.get(id=self.kwargs['pk'])\
            .comment_set.order_by("-pub_date")
        return context


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context


class PostListView(ListView):
    queryset = Post.objects.order_by("-pub_date")


def create_comment(request, post_pk):
    if request.method != "POST":
        raise Http404("Only POST requests supported", request.method)

    form = CommentForm(request.POST)

    if not form.is_valid():
        raise Http404("Invalid form", form.errors)

    post = get_object_or_404(Post, pk=post_pk)

    Comment(text=form.cleaned_data['text'],
            post=post,
            author=request.user).save()

    return HttpResponseRedirect(reverse('blog:post_detail', args=(post_pk,)))
