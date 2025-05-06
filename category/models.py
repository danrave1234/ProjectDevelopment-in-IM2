from django.db import models

# Create your models here.
class Category(models.Model):
    categoryid = models.IntegerField(primary_key=True)
    categoryname = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryname
