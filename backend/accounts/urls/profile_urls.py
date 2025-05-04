from django.urls import path
from ..views.profile_views import get_patch_delete_profile_and_user

urlpatterns = [
    # Profile endpoints
    path('profile/', get_patch_delete_profile_and_user, name="get_patch_delete_profile_and_user" )
]