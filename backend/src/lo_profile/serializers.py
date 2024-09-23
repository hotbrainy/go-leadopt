from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers 
User = get_user_model()

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = "__all__"