from django.db import models


class Group(models.Model):
    text = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField("accounts.User", related_name='user_groups')
    articles = models.ManyToManyField("content.articles", related_name='article_groups')
