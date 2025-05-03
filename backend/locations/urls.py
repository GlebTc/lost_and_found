from django.urls import path
from locations.views.site_views import create_list_all_site, delete_patch_view_site
from locations.views.building_views import create_list_all_building, delete_patch_view_building
from locations.views.level_views import create_list_all_levels

urlpatterns = [
    # Site URLs
    path('sites/', create_list_all_site, name='create_list_all_site'),
    path('sites/<str:site_id>/', delete_patch_view_site, name="delete_patch_view_site"),
    
    # Building URLs
    path('buildings/', create_list_all_building, name='create_list_all_building'),
    path('buildings/<str:building_id>/', delete_patch_view_building, name="delete_patch_view_building"),
    
    # Levels URLs
    path('levels/', create_list_all_levels, name="create_list_all_levels")
    
    # Department URLs
]
