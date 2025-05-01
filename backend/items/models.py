from django.db import models


class Items(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.CharField(max_length=250, blank=True, null=True)
    item_img_url = models.URLField
    found_location
    
