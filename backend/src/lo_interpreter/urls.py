from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from . import views
 
from . import consumers

# Create a router and register our ViewSets with it.
router = DefaultRouter()

# router.register("", views.UserViewSet)
router.register(r'sessions', views.SessionViewSet, basename="sessions")
# router.register(r'messages', views.MessageViewSet, basename="messages")


sessions_router = routers.NestedSimpleRouter(router, r'sessions', lookup='sessions')
sessions_router.register(r'messages', views.MessageViewSet, basename='sessions-messages')

urlpatterns = [               
    # path('index', views.index),
    path("", include(router.urls)),    
    path(r'', include(sessions_router.urls)),
]

websocket_urlpatterns = [                
    path("", consumers.Consumer.as_asgi())
]