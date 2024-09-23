from django.db import models
from django.contrib.auth.models import AbstractUser





class Account(AbstractUser):
    
    avatar = models.ImageField(upload_to='covers/', null=True, blank=True)

    def __str__(self):
        return self.username