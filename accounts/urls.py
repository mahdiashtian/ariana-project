from django.urls import path, include

app_name = "accounts"

urlpatterns = [
    path(f"api/{app_name}/", include(f"accounts.api.urls")),
]
