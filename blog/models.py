import datetime

from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    text = models.TextField(max_length=5000)

    def __str__(self):
        return self.title

    def get_time_passed(self):
        return time_passed_string(self.pub_date)


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

    def get_time_passed(self):
        return time_passed_string(self.pub_date)


def time_passed_string(t):
    """Calculate a '3 hours ago' type string from a python datetime. """
    units = {
        'years': lambda diff: diff.days * 365,
        'months': lambda diff: diff.days * 30,
        'days': lambda diff: diff.days,
        'hours': lambda diff: diff.seconds / 3600,
        'minutes': lambda diff: diff.seconds % 3600 / 60,
    }

    now = timezone.now()
    diff = now - t

    for unit in units:
        dur = int(units[unit](diff))
        if dur > 0:
            # De-pluralize if duration is 1 ('1 day' vs '2 days')
            unit = unit[:-dur] if dur == 1 else unit
            return f'{dur} {unit} ago'
    return 'just now'
