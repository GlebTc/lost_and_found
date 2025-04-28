from django.urls import path
from .views import register_user, login_user, logout_user, own_update_profile, own_delete_profile, get_all_users


urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
    path('update_profile/<str:user_id>/', own_update_profile, name='own_update_profile'),
    path('delete_profile/<str:user_id>/', own_delete_profile, name='own_delete_profile'),
    path('profiles/', get_all_users, name="get_all_users"),   
]
