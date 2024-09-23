from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')

    def __str__(self):
        return self.username