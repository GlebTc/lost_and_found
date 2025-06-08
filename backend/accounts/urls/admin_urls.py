from django.urls import path
from accounts.views.admin_views import (
    CreateListAllProfilesView,
    ProfileAdminDetailView,
)

urlpatterns = [
    path('profiles/', CreateListAllProfilesView.as_view(), name='create_list_all_profiles'),
    path('profiles/<str:user_id>/', ProfileAdminDetailView.as_view(), name='admin-profile-detail'), 
]
