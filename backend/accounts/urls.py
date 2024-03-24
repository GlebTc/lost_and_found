from django.urls import path
from django.http import HttpResponse
from . import views

# API Endpoints
urlpatterns = [
    path('register/', views.register_user, name='register'), #/accounts/register/
    path('login/', views.login_user, name='login'), #/accounts/login/
    path('', views.get_all_users, name='get_all_users'), #/accounts/
    path('edit/<str:user_id>/', views.edit_user, name='edit_user'), #/accounts/edit/<str:user_id>/
]
