from django.urls import path
from accounts.views.admin_views import (
    create_list_all_profiles,
    get_patch_delete_profile_and_user,

)

urlpatterns = [
    path('users/', create_list_all_profiles, name='create_list_all_profiles'),
    path('users/<str:user_id>/', get_patch_delete_profile_and_user), 
]

