from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView, UpdateView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django import forms

from .models import Post, Comment, Profile
from .forms import CommentForm


class HomePageView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_posts"] = Post.objects.order_by("-pub_date")[:4]
        context["popular_posts"] = Post.objects.annotate(num_comm=Count("comment")).order_by("-num_comm")[:4]

        return context


def about(request):
    return render(request, "blog/about.html")


class UserDetailView(DetailView):
    model = User
    template_name = "blog/user_detail.html"
    context_object_name = "userobj"  # don't overwrite "user" object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = User.objects.get(id=self.kwargs['pk'])\
            .comment_set.order_by("-pub_date")
        return context


class ProfileUpdateView(UpdateView, LoginRequiredMixin):
    model = Profile
    fields = ["picture", 'bio']

    def get_object(self):
        print(self.request)
        return self.request.user.profile


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
