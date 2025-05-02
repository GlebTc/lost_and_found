from django.urls import path
from locations.views.site_views import create_list_all_site, delete_patch_view_site
from locations.views.building_views import create_list_all_building, delete_patch_view_building

urlpatterns = [
    # Site URLS
    path('sites/', create_list_all_site, name='create_list_all_site'),
    path('sites/<str:site_id>/', delete_patch_view_site, name="delete_patch_view_site"),
    
    # Building URLS
    path('buildings/', create_list_all_building, name='create_list_all_building'),
    path('buildings/<str:building_id>/', delete_patch_view_building, name="delete_patch_view_building")
]
