from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    text = models.TextField(max_length=5000)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField("date published", auto_now=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,
                               null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.post.pk)])
