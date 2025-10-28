from django.urls import path, include

app_name = "content"

urlpatterns = [
    path(f"api/{app_name}/", include(f"content.api.urls")),
]
