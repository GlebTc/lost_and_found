# Auth URLs
from django.urls import path
from ..views.auth_views import register_user, login_user, logout_user

urlpatterns = [
    # Auth endpoints
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),  
]
