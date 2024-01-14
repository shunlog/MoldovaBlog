from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    text = models.TextField(max_length=5000)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return str(self.id)
