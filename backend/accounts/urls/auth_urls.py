from django.urls import path
from ..views.auth_views import (
    RegisterUserView,
    LoginUserView,
    LogoutUserView,
)

urlpatterns = [
    # Auth endpoints
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
]
