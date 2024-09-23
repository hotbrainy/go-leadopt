from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group #, User

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, viewsets

from lo_user.serializers import UserSerializer, GroupSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    