from django.urls import path
from .views import add_item, get_all_found_items, get_item_by_id, edit_found_item, delete_item

urlpatterns = [
    path('add/', add_item, name='add_found_item'),
    path('', get_all_found_items, name='get_all_found_items'),
    path('<int:item_id>/', get_item_by_id, name='get_item_by_id'),
    path('delete/<int:item_id>/', delete_item, name='delete_item'),
    path('edit/<int:item_id>/', edit_found_item, name='edit_item'),
]
