from rest_framework import serializers
from .models import Chat, Message, Session 

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
        # fields = ["id", 'user', 'title', "created_at", "session_id"]



class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
        # fields = ['session', 'type', "content", "role"]



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        # fields = ["id", 'session', 'type', "content", "language", "code", "output", "role", "created_at"]