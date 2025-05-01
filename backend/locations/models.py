from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)

class Building(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.ForeignKey(Location, related_name="buildings", on_delete=models.CASCADE)

class Level(models.Model):
    number = models.CharField(max_length=25, blank=True, null=True)  # CharField used for levels like Main, B1, L1, etc.
    building = models.ForeignKey(Building, related_name="levels", on_delete=models.CASCADE, blank=True, null=True)

class Department(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    level = models.ForeignKey(Level, related_name="departments", on_delete=models.CASCADE, blank=True, null=True)
