from django.urls import path, include
from utils.views import CsrfTokenView

urlpatterns = [
    path('csrf/', CsrfTokenView.as_view(), name='csrf-token'),
    path('auth/', include('accounts.urls.auth_urls')),
    path('accounts/', include('accounts.urls.profile_urls')),
    path('admin/', include('accounts.urls.admin_urls')),
    path('location/', include('locations.urls')),
    path('', include('items.urls'))
]
