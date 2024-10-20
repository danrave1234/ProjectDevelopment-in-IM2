from django.db import models

# Create your models here.
class Location(models.Model):
    locationid = models.IntegerField(primary_key=True)
    building = models.CharField(max_length=50)
    floor = models.CharField(max_length=50)