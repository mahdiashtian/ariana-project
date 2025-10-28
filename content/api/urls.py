from django.urls import path, include
from rest_framework.routers import DefaultRouter

from content.api.article.article_api import ArticleViewSet
from content.api.group.group_api import GroupViewSet

router = DefaultRouter()
router.register("article", ArticleViewSet, basename="article")
router.register("group", GroupViewSet, basename="group")
urlpatterns = router.urls
