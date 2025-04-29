from django.urls import path
from ..views.profile_views import own_delete_profile, own_update_profile, get_all_users

urlpatterns = [
    # Profile endpoints
    path('profile/update/', own_update_profile, name='own_update_profile'),
    path('profile/delete/', own_delete_profile, name='own_delete_profile'),
    path('profiles/', get_all_users, name="get_all_users"),   
]