from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our ViewSets with it.
router = DefaultRouter()
 
router.register("", views.ProfileViewSet)


urlpatterns = [                
    path("", include(router.urls)),
]