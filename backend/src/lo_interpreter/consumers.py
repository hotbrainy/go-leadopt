import json
import time
import jwt
import asyncio
import uuid
import os

from django.contrib.auth import get_user_model
from django.conf import settings

from asgiref.sync import sync_to_async

from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from interpreter import OpenInterpreter, AsyncInterpreter

from . import models
from .serializers import ChatSerializer, MessageSerializer, SessionSerializer


User = get_user_model()
agents = {}

class Consumer2(WebsocketConsumer):
    def connect(self):
        self.accept()
        while int(1) in Queue.objects.all().values_list('status', flat=True):
            self.send(text_data=json.dumps({"value":Random.objects.all().count()}))
            Random.objects.create(text = "test")
            time.sleep(2)
        self.close()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data=text_data)
        self.close()
         

class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.__init__()
        self.user = None
        # print("============session_id=-=================")
        # print(self.session_id)
        # if self.scope['query_string'] is None or self.scope['query_string'] == b'':
        #     await self.close()
        #     return
        # print(self.scope['query_string'])
        # self.token = self.scope['query_string'].decode().split('=')[1]
        # self.user = await self.authenticate_user(self.token)
        
        # if self.user is None:
        #     await self.close()
        # else:
            # self.session = await sync_to_async(models.Session.objects.get)(session_id=uuid.UUID(self.session_id))
            # self.session_group = f'chat_{self.session.id}'
            # self.interpreter = AsyncInterpreter()
            # self.interpreter.auto_run = True
            # msgs = await self.get_messages(self.session.id)
            # self.interpreter.custom_instructions=f"""
            # Here the chat history.
            # {msgs}
            # """
            # self.interpreter.messages = await self.get_messages(self.session.id)
        await self.accept()
            # print(self.interpreter.custom_instructions)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        
        data = json.loads(text_data)
        # Handle incoming WebSocket data
        # data["session"] =  self.session.id
        # data["user_id"] = self.user["id"] 
        
        match data.get("type"):
            case "auth":
                # print(f"auth - {data}")
                self.user = await self.authenticate_user(data.get("token"))
                # print(self.user)
                if not self.user:
                    await self.send(text_data=json.dumps({'error': 'Authentication required'}))
                await self.send(text_data=json.dumps({"type":"auth", 'message':"Authentication successed", "user":self.user.username}))
                self.user_folder = self.create_user_folder(self.user)
                return
            case "interpreter":
                if not self.user:
                    await self.send(text_data=json.dumps({'error': 'Authentication required'}))
                    return
                if data.get("action") == "init":
                    self.interpreter = AsyncInterpreter()
                    self.interpreter.auto_run = True
                    self.interpreter.custom_instructions=f"""
                    You are a sales manager who is familiar with Open Interpreter. Your duty is to manage sales - you can connect to mongodb with uri and interact with databases, and users' requirement for linkedin profiles whilst also being able to interact with these people.
                    You are a sales manager, harvesting, analysing and contacting a network and new leads. contacts can be accessed at Mongo Database URI: 'mongodb://localhost:27017/' in the `lead_opt` database, the list called `r2001` is composed of contacts and leads. if asked for contacts and leads you will assume `r2001` is where they are stored. the database is made up of people at construction companies. where as an an example the materials column lists the materials used, you will have an in-depth understanding of services that they will require to complete their development. All answers will be given in as few words as possible. no formalities, no boiler plates - focus on sales, efficiency and making money. give your answers with images where it is helpful and offers quick analysis. assume the person reading your answers is very smart and doesn't want any non-essential information.
                    When you search data, ignore the case. and the field names maybe upper case.
                    Before you  start get all data, you need to connect to database and get all data from the collection `r2001`.
                    Your max chat response length is 4000 characters but sometimes the user will need large data provided. when large data is requested first you will ask the user if you should save the data to a file and if so provide a link to download the file.
                    You have to save the data to the `{self.user_folder}` folder and provide the link.
                    `{self.user_folder} `is static folder in the project root.
                    when you generate the link, the link should be in the format of `/static/{self.user.username}/result_{self.user.username}_dateme.csv`
                    """
                    # print(self.interpreter.custom_instructions)
                    # print(f"chat - {data}")
                    if data.get("session_id") is None:
                        await self.send(text_data=json.dumps({"type":"interpreter", "action":"init", 'message':"Interpreter initialized.", "session":"null"}))
                    else:
                        # print(data.get("session_id"))
                        self.session_id = data.get("session_id")
                        self.session = await sync_to_async(models.Session.objects.get)(session_id=uuid.UUID(data.get("session_id")))
                        msgs = await self.get_messages(self.session.id)
                        self.interpreter.messages = await self.get_messages(self.session.id)
                        # self.session_group = f'chat_{self.session.id}'
                        # self.interpreter = AsyncInterpreter()
                        # self.interpreter.auto_run = True
                        # self.interpreter.custom_instructions=f"""
                        # Here the chat history.
                        # {msgs}
                        # """
                        await self.send(text_data=json.dumps({"type":"interpreter", "action":"init", 'message':"Interpreter initialized.", "session":self.session.title}))
                elif data.get("action") == "chat":
                    chatdata = data["payload"]
                    chatdata["session"] = self.session.id
                    chat = await self.save_data(chatdata)
                    if "content" in chat:
                        prompt = chat["content"]
                        chat["message"] = chat["content"]
                        if prompt is not None and prompt != "":
                            # try:
                            msgs = []
                            full_response = ""
                            current_msg ={}
                            for chunk in self.interpreter.chat(chat, stream=True, display=False):
                                # print(chunk)
                                await asyncio.sleep(0.001)
                                if isinstance(chunk, dict):
                                    if chunk.get("type") == "message" and chunk.get("start" )== True:
                                        current_msg = chunk
                                    if chunk.get("type") == "message":
                                        full_response += chunk.get("content", "")
                                    await self.send(text_data = json.dumps({"payload":chunk, "type":"interpreter", "action":"chat"}))
                                    
                                    if chunk.get("type") == "message" and chunk.get("end") == True:
                                        current_msg["content"] = full_response
                                        # current_msg["message"] = full_response
                                        current_msg["session"] = self.session.id
                                        msgs.append(current_msg)
                                        # print(f"msgs: {msgs}")
                                        
                                elif isinstance(chunk, str):
                                    # Attempt to parse the string as JSON
                                    try:
                                        json_chunk = json.loads(chunk)
                                        full_response += json_chunk.get("response", "")
                                        await self.send(text_data = json.dumps({"payload":chunk, "type":"interpreter", "action":"chat"}))
                                    except json.JSONDecodeError:
                                        # If it's not valid JSON, just add the string
                                        full_response += chunk

                            await self.save_messages([chat])
                            await self.save_messages(msgs)
                            if self.session.title == "New Session":
                                await self.update_session_title(chat, msgs)
                            # except Exception as e:
                            #     print(f"error: {e}")
                            #     return await self.send(text_data=json.dumps({'status': 'error', 'errors': str(e)}))
                        else:
                            pass
                    else:
                        await self.send(text_data=json.dumps({'status': 'error', 'errors': "no prompt"}))
 
            case "chat":
                print(f"chat - {data}")
 

    def create_user_folder(self, user):
        # Define the path to the user's folder
        user_dir = os.path.join(settings.BASE_DIR, 'static', user.username)

        # Check if the directory does not exist, then create it
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return user_dir
    
    @database_sync_to_async
    def update_session_title(self, chat, msgs):
        # print(f"chat - {chat}")
        summarizer = OpenInterpreter()
        message = summarizer.chat(f"""Give me a short title for summarizing this chat in plain text format, not in markdown, not contain database name or type or collection name.
                              {chat}
                              {msgs}
                              """, display=False) 
        del summarizer
        session_serializer = SessionSerializer(self.session, data={"title":message[0]["content"]}, partial=True)
        if session_serializer.is_valid():
            session_serializer.save()
            return session_serializer.data
        else:
            print(session_serializer.errors)

        
    @database_sync_to_async
    def get_messages(self, session_id):       
        msgs = models.Message.objects.filter(session_id=session_id)
        serialized_msgs = MessageSerializer(msgs, many=True).data  # Serialize the queryset
        return serialized_msgs
    
    @database_sync_to_async
    def save_data(self, data):       
    
        serializer = ChatSerializer(data=data)
        is_valid =  serializer.is_valid()
        if is_valid:
            # serializer.save()
            return serializer.data
        else:
            # await self.send(text_data=json.dumps({'status': 'error', 'errors': serializer.errors}))
            print(serializer.errors)

    @database_sync_to_async
    def save_messages(self, msgs):       
        for msg in msgs:
            serializer = MessageSerializer(data=msg)
            is_valid =  serializer.is_valid()
            if is_valid:
                serializer.save()
            else:
                # await self.send(text_data=json.dumps({'status': 'error', 'errors': serializer.errors}))
                print(serializer.errors)

    
    @database_sync_to_async
    def authenticate_user(self, token):
        try:
            # Decode the token
            # payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            # print(payload['user_id'])
            user = User.objects.get(id=1)
            print(user.username)
            return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None