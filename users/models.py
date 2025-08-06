from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=160, blank=True, null=True)
    website = models.URLField(max_length=200, blank=True, null=True)