from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # this class consists of requested item as it is unique to each user
    pass


class MyQueries(models.Model):
    # this class consists of my queries as it is unique to each user
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user id is unique to each user
    query = models.TextField() # query is unique to each user
    date = models.DateTimeField(auto_now_add=True) # date of query
    results = models.JSONField() # results of query

    def __str__(self):
        return self.query