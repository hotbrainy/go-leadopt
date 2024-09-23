from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group #, User

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, viewsets

from .models import Profile

from lo_profile.serializers import ProfileSerializer

User = get_user_model()
 

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Profile.objects.all().order_by('user')
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    