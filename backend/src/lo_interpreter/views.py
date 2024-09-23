import uuid

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import Group #, User
from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Session, Message


from lo_interpreter.serializers import  SessionSerializer, MessageSerializer


# Create your views here.

def index(request):
    return render(request, 'index.html')



class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    



class SessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # authentication_classes = [JWTAuthentication]
    # queryset = Session.objects.all().order_by('-created_at')
    serializer_class = SessionSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Override get_queryset to filter sessions by the authenticated user 
        # return Session.objects.filter(user= self.request.user).order_by('-created_at')
        return Session.objects.filter(user=1).order_by('-created_at')

    
    def create(self, request, *args, **kwargs):  
        # Create a new session instance
        session_data = request.data.copy()
        session_data['user'] = 1 #request.user.id

        serializer = self.get_serializer(data=session_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    # authentication_classes = [JWTAuthentication]
    queryset = Message.objects.all()  # Make sure this is defined correctly
    serializer_class = MessageSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    
    def get_queryset(self):
        # q = int(self.request.query_params.get("page", 1))
        
        session_id =  uuid.UUID(self.kwargs.get("sessions_pk"))
           # Filter messages based on session_id, which is the primary key of the Session model
        session = None
        try:
            # Find the session using the custom session_id field
            session = Session.objects.get(session_id=session_id)
        except Session.DoesNotExist:
            raise NotFound(detail=f"Session not found with given session_id {session_id}.") 
        
        # Override get_queryset to filter sessions by the authenticated user  
        if session is not None:
            return Message.objects.filter(session_id=session.id).order_by('created_at')
        else:
            raise NotFound(detail=f"Session not found with given session_id {session_id}.") 
    
    @action(detail=False, methods=['get'], url_path='all')
    def all_items(self, request, *args, **kwargs):
        # Extract the nested parameter if needed
        sessions_pk =  uuid.UUID(kwargs.get('sessions_pk', None))
        print(f"session-pk-{sessions_pk}")
        # Filter based on the nested parameter, if applicable
        session = None
        try:
            # Find the session using the custom session_id field
            session = Session.objects.get(session_id=sessions_pk)
        except Session.DoesNotExist:
            raise NotFound(detail=f"Session not found with given sessions_pk {sessions_pk}.") 
        
        
        if session is not None:
            items = self.queryset.filter(session_id=session.id)
        else:
            items = self.queryset

        serializer = self.get_serializer(items, many=True)
        return Response(serializer.data)