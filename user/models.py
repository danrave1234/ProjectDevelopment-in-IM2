from django.db import models

# Create your models here.
class User(models.Model):
    userid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

