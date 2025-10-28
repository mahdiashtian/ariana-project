from django.db import models

from content.models.articles import Article


class Group(models.Model):
    text = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField("accounts.User", related_name='user_groups')
    articles = models.ManyToManyField(Article, related_name='article_groups')
