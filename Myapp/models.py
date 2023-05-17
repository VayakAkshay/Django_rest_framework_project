from django.db import models
from django.contrib.auth.models import User
import datetime

# class UserData(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=100)
#     password = models.TextField(max_length=20)


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    content = models.TextField(max_length=1000)
    creation_date = models.DateField(default=datetime.date.today)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    private = models.BooleanField()
    total_likes = models.IntegerField(default=0)

class LikeData(models.Model):
    like_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)