from django.urls import path
from accounts.views.admin_views import get_all_users

urlpatterns = [
    path('users/', get_all_users, name='get_all_users'),  # Final path: /api/v1/admin/users/
]
