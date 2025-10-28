from django.urls import path

from accounts.api.auth.auth_api import TokenObtainPairApi
from accounts.api.change_password.change_password_api import ChangePasswordApi
from accounts.api.me.me_api import MeApi
from accounts.api.refresh.refresh_api import TokenRefreshApi
from accounts.api.verify.verify_api import TokenVerifyApi

urlpatterns = [
    path('auth/', TokenObtainPairApi.as_view()),
    path('me/', MeApi.as_view()),
    path('verify/', TokenVerifyApi.as_view()),
    path('refresh/', TokenRefreshApi.as_view()),
    path('change-password/', ChangePasswordApi.as_view())
]
