from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group #, User

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions, viewsets

from .models import LinkedIn, Contact

from lo_profile.serializers import LinkedInSerializer, ContactSerializer

User = get_user_model()
 

class LinkedInViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = LinkedIn.objects.all()
    serializer_class = LinkedInSerializer
    # permission_classes = [permissions.IsAuthenticated]
    

class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    # permission_classes = [permissions.IsAuthenticated]
    