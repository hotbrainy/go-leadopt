from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers 
from .models import LinkedIn, Contact
# User = get_user_model()

class LinkedInSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = LinkedIn
        fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Contact
        fields = "__all__"