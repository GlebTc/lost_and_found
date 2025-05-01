from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)

class Building(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, related_name="buildings", on_delete=models.CASCADE)

class Level(models.Model):
    number = models.CharField(max_length=25)  # or CharField if you want L1, B1, etc.
    building = models.ForeignKey(Building, related_name="levels", on_delete=models.CASCADE)

class Department(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(Level, related_name="departments", on_delete=models.CASCADE)
