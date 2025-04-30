from django.urls import path
from accounts.views.admin_views import get_all_users, get_individual_user_info, update_user

urlpatterns = [
    path('users/', get_all_users, name='get_all_users'),
    path('users/<str:user_id>/', get_individual_user_info, name='get_individual_user_info'),
    path('users/<str:user_id>/update/', update_user, name='update_user'),

]
