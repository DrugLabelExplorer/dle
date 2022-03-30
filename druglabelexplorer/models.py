from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    #this class consists of requested item as it is unique to each user
    requesteditem = models.ManyToManyField("Item")


class Item(models.Model):
    #this class consists of features users inspect 
    active = models.BooleanField(default=True)
    timeadded = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    contributor = models.ForeignKey(
        "User", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=0)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Tracking(models.Model):
    #this class provides features for user to monitor tracking and storage history
    content = models.TextField(blank=True)
    tracker = models.ForeignKey("User", on_delete=models.CASCADE)
    timeadded = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(
        "Item", on_delete=models.CASCADE, related_name="trackings")

    def __str__(self):
        return self.content
