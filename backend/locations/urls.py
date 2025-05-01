from django.urls import path
from locations.views.site_views import create_site, delete_site

urlpatterns = [
    path('site/create/', create_site, name='create_site'),
    path('site/delete/<str:site_id>/', delete_site, name="delete_site"),
]
