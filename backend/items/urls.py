from django.urls import path
from .views import create_get_all_items

urlpatterns = [
    path('items/', create_get_all_items, name='create_get_all_items'),
]
