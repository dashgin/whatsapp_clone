from django.contrib.auth import views as django_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', django_views.LoginView.as_view(), name='login'),
    path('logout/', django_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
