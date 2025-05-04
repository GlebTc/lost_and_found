from django.db import models
import uuid
from locations.models import Site, Building, Level, Department
from accounts.models import Profile

class Items(models.Model):
    # Item Status Choices
    STATUS_CHOICES = [
    ('lost', 'lost'),
    ('found', 'found'),
    ('claimed', 'claimed'),
]
    
    # Item Fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    item_img_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, blank=False, null=False)
    owner_identified = models.BooleanField(default=False)
    owner_name = models.CharField(max_length=150, blank=True, null=True)
    owner_contact = models.CharField(max_length=150, blank=True, null=True)
    date_reported_turned_in = models.DateField(auto_now_add=True)
    date_claimed_returned = models.DateField(auto_now_add=True)
    accepted_by = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        # The Profile foreign key could also be set to on_delete=models.PROTECT.  This is a stricter approach as it prevents deleting any of the users unless all connected items have also been deleted.  This would prevent user cleanup in the future.  For that reason, a hybrid approach is used.  The delete is set to SET_NULL and additional field below, accepted_by_name, keeps track of the name of the person that accepted the item while allowing removeal of foreign key.
        # IMPORTANT: The accepted_by_name will be used as fall back value on front end.
        blank=False,
        null=True,
        related_name="accepted_items"
        # This allows for one-to-many relationship where one Profile can accept many Items but each Item can only be accepted by on Profile.  Example code:
            # user = Profile.objects.get(id="some-user-id")
            # items = user.accepted_items.all()
    )
    accepted_by_email = models.CharField(max_length=250, blank=False, null=False)
    turned_in_by_name = models.CharField(max_length=150, blank=True, null=True)
    turned_in_by_phone = models.CharField(max_length=20, blank=True, null=True)
    claimed_by_id_verified = models.BooleanField(default=False)
    claimed_by = models.CharField(max_length=150, blank=False, null=False)
    item_returned_by = models.ForeignKey(
        Profile,
            on_delete=models.SET_NULL,
            blank=True,
            null=True,
            related_name="returned_items"
        )
    item_returned_by_name=models.CharField(max_length=250, blank=True, null=True)
    
    # Location Fields
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, blank=True, null=True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} ({self.status})"