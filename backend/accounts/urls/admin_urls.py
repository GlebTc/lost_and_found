from django.urls import path
from accounts.views.admin_views import (
    get_all_users,
    get_individual_user_info,
    update_user,
    delete_user,
    create_user
)

urlpatterns = [
    path('users/', get_all_users, name='get_all_users'),
    path('users/create/', create_user, name='create_user'),
    path('users/<str:user_id>/', get_individual_user_info, name='get_individual_user_info'),
    path('users/<str:user_id>/update/', update_user, name='update_user'),
    path('users/<str:user_id>/delete/', delete_user, name='delete_user'),
]

