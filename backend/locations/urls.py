from django.urls import path
from locations.views.site_views import create_list_all_site, get_patch_delete_site
from locations.views.building_views import create_list_all_building, get_patch_delete_building
from locations.views.level_views import create_list_all_levels, get_patch_delete_level

urlpatterns = [
    # Site URLs
    path('sites/', create_list_all_site, name='create_list_all_site'),
    path('sites/<str:site_id>/', get_patch_delete_site, name="get_patch_delete_site"),
    
    # Building URLs
    path('buildings/', create_list_all_building, name='create_list_all_building'),
    path('buildings/<str:building_id>/', get_patch_delete_building, name="get_patch_delete_building"),
    
    # Levels URLs
    path('levels/', create_list_all_levels, name="create_list_all_levels"),
    path('levels/<str:level_id>/', get_patch_delete_level, name="get_patch_delete_level")
    
    # Department URLs
]
