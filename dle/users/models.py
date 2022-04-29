from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # this class consists of requested item as it is unique to each user
    #pass
    liked_posts = models.ManyToManyField(
        "Post", blank=True, related_name="likers")

class MyQueries(models.Model):
    # this class consists of my queries as it is unique to each user
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user id is unique to each user
    query = models.TextField() # query is unique to each user
    date = models.DateTimeField(auto_now_add=True) # date of query
    results = models.JSONField() # results of query

    def __str__(self): 
        return self.query
        

class Post(models.Model):
    # Post class includes author/account, post contents and timestamp
    # referenced prior lecture notes
    author = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts_created")
    content = models.CharField(max_length=1000) #this would be the drug label in search results
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content[:10]} {self.author.username}"        