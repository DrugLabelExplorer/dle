from django.db import models
from django.contrib.auth.models import AbstractUser
from data.models import DrugLabel

class User(AbstractUser):
    pass

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

# like
class Like(models.Model):

    post = models.ForeignKey(Post,on_delete= models.CASCADE,related_name="Post")
    user = models.ManyToManyField(User,blank =True,related_name="user_info")

    def __str__(self):
        return f"{self.user} liked {self.post}"


class MyLabel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drug_label = models.ForeignKey(DrugLabel, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, db_index=True)
    file = models.FileField(upload_to="my_labels/", max_length=255)
    is_successfully_parsed = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return (
            f"MyLabel: {self.id}, "
            f"user: {self.user}, "
            f"drug_label: {self.drug_label}, "
            f"name: {self.name}, "
            f"file.name: {self.file.name}, "
            f"is_successfully_parsed: {self.is_successfully_parsed}"
        )        
