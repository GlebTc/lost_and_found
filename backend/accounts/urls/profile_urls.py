from django.urls import path
from ..views.profile_views import classProfileDetailView

urlpatterns = [
    # Profile endpoints
    path('profile/', classProfileDetailView.as_view(), name="get_patch_delete_profile_and_user" )
]