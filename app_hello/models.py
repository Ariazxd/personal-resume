from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True)
    phone = models.CharField(max_length=50, null=True)
    job_title = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    intrests = models.TextField(null=True)
    location = models.CharField(null=True, max_length=70)

    def __str__(self):
        return self.user.username


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=50, null=True)
    date_range = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=100, null=True)
    job_description = models.CharField(null=True, max_length=100)


class Education(models.Model):
    DEGREE_CHOICES = [
        ('Diploma', 'High School Diploma'),
        ('associate', 'Associate Degree'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('phd', 'PhD'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    university = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=50, null=True)
    date_range = models.CharField(max_length=50, null=True)
    degree = models.CharField(max_length=100, null=True, choices=DEGREE_CHOICES)
    study_description = models.CharField(null=True, max_length=100)

    @property
    def pretified_degree(self):
        return dict(self.DEGREE_CHOICES).get(self.degree)


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)


class Skill(models.Model):
    LEVEL_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50, null=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, null=True, default=1)
