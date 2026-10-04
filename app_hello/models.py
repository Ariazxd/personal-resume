from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50,null=True)
    job_title = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)


class Experience(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=50,null=True)
    date_range = models.CharField(max_length=50,null=True)
    position = models.CharField(max_length=100,null=True)
    job_description = models.CharField(null=True,max_length=100)
