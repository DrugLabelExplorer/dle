from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # this class consists of requested item as it is unique to each user
    pass


class MyQueries(models.Model):
    # this class consists of my queries as it is unique to each user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    results = models.JSONField()

    def __str__(self):
        return self.query