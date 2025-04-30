from django.urls import path
from ..views.profile_views import own_delete_profile, own_update_profile, own_view_profile

urlpatterns = [
    # Profile endpoints
    path('profile/update/', own_update_profile, name='own_update_profile'),
    path('profile/delete/', own_delete_profile, name='own_delete_profile'),
    path('profile/', own_view_profile, name="own_view_profile" )
]