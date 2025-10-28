from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.api.auth.auth_api import TokenObtainPairApi
from accounts.api.change_password.change_password_api import ChangePasswordApi
from accounts.api.knowledge.knowledge_api import KnowledgeViewSet
from accounts.api.me.me_api import MeApi
from accounts.api.refresh.refresh_api import TokenRefreshApi
from accounts.api.verify.verify_api import TokenVerifyApi

router = DefaultRouter()
router.register("knowledge", KnowledgeViewSet, basename="knowledge")
urlpatterns = [
    path('auth/', TokenObtainPairApi.as_view()),
    path('me/', MeApi.as_view()),
    path('verify/', TokenVerifyApi.as_view()),
    path('refresh/', TokenRefreshApi.as_view()),
    path('change-password/', ChangePasswordApi.as_view()),
    path('', include(router.urls))
]
