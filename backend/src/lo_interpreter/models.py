import uuid
from django.db import models
 
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# Create your models here.

class Session(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_id = models.UUIDField(max_length=255, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="New Session")
    created_at = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    id = models.BigAutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='chats')
    type = models.CharField(max_length=255, blank=True,null=True)
    role = models.CharField(max_length=255, blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    
class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='messages')
    type = models.CharField(max_length=255, blank=True,null=True)
    role = models.CharField(max_length=255, blank=True,null=True)
    content = models.TextField(blank=True,null=True)
    # message = models.TextField(blank=True,null=True)
    language = models.CharField(max_length=255, blank=True,null=True)
    code = models.TextField(blank=True,null=True)
    output = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    