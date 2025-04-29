from .auth_urls import urlpatterns as auth_urlpatterns
# from .profile_urls import urlpatterns as profile_urlpatterns

# Combine all URL patterns together
urlpatterns = auth_urlpatterns
