from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import utils


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(blank=True,
                                validators=[utils.file_size_validator(2)],
                                help_text="Maximum file size is 2 MiB")
    bio = models.TextField(max_length=1000, blank=True)

    @receiver(post_save, sender=User)
    def on_user_create(sender, instance, created, **kwargs):
        '''Create a profile for new users automatically'''
        if not created:
            return
        p = Profile.objects.create(user=instance)
        p.save()

    def get_absolute_url(self):
        return reverse('blog:user_detail', args=[str(self.user.pk)])

    def role(self):
        if self.user.is_staff:
            return 'Author'

        return 'Commenter'


class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    text = models.TextField(max_length=5000)
    location = models.CharField(max_length=1000, blank=True)
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.pk)])

    def get_time_passed(self):
        return utils.time_passed_string(self.pub_date)


class Image(models.Model):
    file = models.ImageField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    alt = models.CharField(max_length=500, blank=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.file.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    pub_date = models.DateTimeField("date published", auto_now=True)
    author = models.ForeignKey(get_user_model(),
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    def __str__(self):
        try:
            name = self.author.username
        except:
            name = '[]'
        return f'{name}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[str(self.post.pk)])\
            + '#' + str(self.pk)

    def get_time_passed(self):
        return utils.time_passed_string(self.pub_date)
