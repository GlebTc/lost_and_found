from django.urls import path
from locations.views.site_views import sites_list_create, delete_patch_view_site
from locations.views.building_views import create_building

urlpatterns = [
    # Site URLS
    path('sites/', sites_list_create, name='create_site'),
    path('sites/<str:site_id>/', delete_patch_view_site, name="delete_patch_view_site"),
    
    # Building URLS
    path('buildings/', create_building, name='create_building'),
]
