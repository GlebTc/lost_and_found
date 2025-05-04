from django.urls import path
from .views import create_get_all_items, get_patch_delete_item

urlpatterns = [
    path('items/', create_get_all_items, name='create_get_all_items'),
    path('items/<str:item_id>/', get_patch_delete_item, name="get_patch_delete_item")
]
