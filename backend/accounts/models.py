from django.db import models

class Profile(models.Model):
    id = models.UUIDField(primary_key=True)
    # The id is dynamically set when the user registers in accounts/views/auth_views.py from the response provided by supabase auth.
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, default='user')
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    avatar_url = (models.URLField(blank=True, null=True))
    
    def __str__(self):
        return f"{self.email} ({self.role})"
