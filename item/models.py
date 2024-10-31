from django.db import models

from category.models import Category
from location.models import Location


# Create your models here.
class Item(models.Model):
    itemid = models.AutoField(primary_key=True)
    itemname = models.CharField(max_length=50)
    itemdescription = models.TextField()
    date = models.DateField(auto_now=True)
    categoryid = models.ForeignKey(Category, on_delete=models.CASCADE)
    locationid = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="unclaimed")
