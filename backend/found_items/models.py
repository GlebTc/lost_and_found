from django.db import models
import uuid

class FoundItem(models.Model):
    date_received = models.DateField(blank=True, null=True)
    log_item_number = models.UUIDField(default=uuid.uuid4, editable=False)
    found_location = models.CharField(max_length=100, blank=True, null=True)
    item_description = models.TextField(blank=False)
    received_by = models.CharField(max_length=100, blank=False)
    turned_in_by = models.CharField(max_length=100, blank=True, null=True)
    claimed_by = models.CharField(max_length=100, blank=True, null=True)
    released_by = models.CharField(max_length=100, blank=True, null=True)
    date_released = models.DateField(blank=True, null=True)
    archived = models.BooleanField(default=False)
