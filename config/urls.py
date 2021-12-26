from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("accounts/", include("allauth.urls")),
    path("", include("chat.urls")),
    path("accounts/", include('django.contrib.auth.urls')),
]
