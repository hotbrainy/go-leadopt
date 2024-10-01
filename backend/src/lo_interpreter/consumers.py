from datetime import timedelta
import json
import time
import jwt
import asyncio
import uuid
import os
import pytz
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

from asgiref.sync import sync_to_async

from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer

# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser

from interpreter import OpenInterpreter, AsyncInterpreter

from . import models
from .serializers import ChatSerializer, MessageSerializer, SessionSerializer
from lo_profile.models import LinkedIn
from lo_profile.serializers import LinkedInSerializer

User = get_user_model()
agents = {}

connected_users = {}
 
class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.__init__()
        self.user = None
        self.room_name = "chat"
        self.room_group_name = 'group_chat'
        print(self.channel_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
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
                if data.get("sender", "app") == "chrome":
                    # self.channel_name = f"chrome_{self.user.username}"
                    connected_users[f"{self.user.username}_chrome"] = self.channel_name
                else:
                    connected_users[self.user.username] = self.channel_name
                return
            case "interpreter":
                if not self.user:
                    await self.send(text_data=json.dumps({'error': 'Authentication required'}))
                    return
                match data.get("action"):
                    case "init":
                        self.interpreter = AsyncInterpreter()
                        self.interpreter.auto_run = True
                        self.interpreter.custom_instructions=f"""
                        # PERSONALITY
                        Your name is Bob.
                        You are a sales manager. You are familiar with Open Interpreter. Your duty is to manage sales - you can connect to PostgreSQL and interact with databases, and users' requirement for linkedin profiles whilst also being able to interact with these people.
                        You are a sales manager, harvesting, analysing and contacting a network and new leads. contacts can be accessed at PostgreSQL Database.
                        # DATABASE
                        The database credentials are as follows:
                        host: localhost
                        port: 5432
                        user: postgres
                        password: root
                        database: leadopt
                        prefix: lo_
                        In the database which you will connect to automatically, the list called `lo_profile_contact` is composed of contacts and leads. if asked for contacts and leads you will assume `lo_profile_contact` is where they are stored. the database is made up of people at construction companies. where as an an example the materials column lists the materials used, you will have an in-depth understanding of services that they will require to complete their development. 
                        At the start, get all data from the database - you need to connect to database in the background and get all data from the collection `lo_profile_contact`.
                        All field names are in uppercase. So if you are asked for a field name, you will assume it is in uppercase. For example, if you are asked for the first name, you will assume it is `FIRST_NAME`.
                        Here’s a simplified breakdown of the fields, assuming they're for managing construction projects:

                            PROJECTID: Unique identifier for the project.
                            HEADING: Short title or description of the project.
                            PROJECT_NAME: The full name of the project.
                            ADDRESSLINE1, ADDRESSLINE2, ADDRESSLINE3: Lines for the project’s address, broken down for detailed formatting.
                            TOWN, BOROUGH, COUNTY: The town, borough, and county where the project is located.
                            POSTCODE: Postal code of the project site.
                            GOV_REGION: Government region where the project is located.
                            VALUE: The monetary value of the project.
                            VALUETYPE: Type of value (e.g., estimated, contract value).
                            PLANNINGSTAGE: Current stage in the planning process.
                            CONTRACTSTAGE: Current stage in the contracting process.
                            STARTDATE, STARTDATETYPE: Project start date and type (e.g., estimated or confirmed).
                            ENDDATE, ENDDATETYPE: Project end date and type (e.g., estimated or confirmed).
                            CONTRACTPERIOD: Duration of the contract (e.g., in months).
                            DEV_TYPE: Type of development (e.g., residential, commercial).
                            PROJECT_SIZE: The size of the project (could refer to cost, scale, or area).
                            PROJECTSTATUS: Current status (e.g., in progress, completed).
                            SITE_AREA: Total area of the project site.
                            FLOORAREA: Total floor area being constructed.
                            UNITS: Number of units (e.g., apartments).
                            STOREYS: Number of storeys/floors in the project.
                            PRIMARYSECTORS: The main sectors involved (e.g., housing, infrastructure).
                            PRIMARYCATEGORY: Main category of the project (e.g., construction, refurbishment).
                            SECTOR_GROUP: Group to which the sector belongs (e.g., private or public).
                            MATERIALS: Key materials used in the project (e.g., concrete, steel).
                            LATESTINFORMATION: The most recent updates or changes in the project.
                            SCHEMEDESCRIPTION: Detailed description of the project plan or scheme.
                            LEADPLANNINGAPPLICATIONNUMBER: Reference number for the main planning application.
                            LEAD_APPLICATION_SUBMITTED_DATE: Date the lead planning application was submitted.
                            LEAD_APPLICATION_DECISION_DATE: Date a decision was made on the application.
                            DECISION: Outcome of the planning application (e.g., approved, rejected).
                            COUNCILNAME: Name of the council responsible for the project.
                            RECORD_TYPE: Type of record (e.g., planning, construction).
                            ROLE_NAME: The role of the contact person (e.g., architect, project manager).
                            SALUTATION, FIRST_NAME, LAST_NAME: Contact person’s title (e.g., Mr., Ms.), first and last name.
                            HAS_LINKEDIN_URL: Indicates whether the contact has a LinkedIn profile (True/False).
                            LINKEDIN_URL: The LinkedIn profile URL of the contact.
                            JOB_TITLE: Job title of the contact.
                            PHONE: Contact’s office phone number.
                            MOBILE: Contact’s mobile phone number.
                            PERSONALEMAIL: Contact’s personal email.
                            LAST_CHECKED_DATE: Last date the contact information was updated.
                            OFFICE_NAME: Name of the office responsible for the project.
                            OFFICE_ID: Unique identifier for the office.
                            ADDR_1, ADDR_2, ADDR_3: Address lines for the office.
                            TOWN_NAME, COUNTY_NAME, POST_CD: Town, county, and postal code for the office.
                            OFF_GOV_REGION: Government region where the office is located.
                            SHOULD_UPDATE: Indicates whether the contact information needs to be updated by harvester.(True/False)
                        # STYLE
                        All answers will be given in as few words as possible. don't say "i'll update the code" or "i'll write a function" - just do it.
                        I need the very precise and concise answer as less as possible.
                        The simpler, the better. Ideal answer is only one word. This is very important.
                        don't send any answers as a code block or report on the code you are executing.
                        No formalities, no boiler plates, use as few words as possible to give the answer only - focus on sales, efficiency and making money.
                        Give your answers with images where it is helpful and offers quick analysis. 
                        Assume the person reading your answers is very smart and doesn't want any non-essential information, code or explanation unless requested.
                        Don't offer further help.
                        All links  should be opened in a new window so that keeps the current tab.
                        All data will be provided in the format of a plain text, not json or code format.
                        Your max chat response length is 4000 characters but sometimes the user will need large data provided. when large data is requested first you will ask the user if you should save the data to a file and if so provide a link to download the file.
                        You have to save the data to the `{self.user_folder}` folder and provide the link.
                        `{self.user_folder} `is static folder in the project root.
                        when you generate the link, the link should be in the format of `/static/{self.user.username}/result_{self.user.username}_dateme.csv`. The links should be full url. host name is localhost and port is 8000. 
                       

                        # DATA
                        When searching data, ignore the case.
                        When provided with part of the data e.g. name and company, you will add this and leave the other fields blank.
                        The name would be full name, so interpet this as first name and last name. The company name might not the full name of the company (e.g. SEGRO = SEGRO Plc; words such as UK Ltd should be ignored.)
                        If you add a new contact, harvester chrome extension will be used to get the data.
                        if you are asked to the data again, you need to re run the query to get the updated data.
                        If you are asked to update the data with harvester, you have to update the field 'SHOULD_UPDATE' with boolean value True. The harverster chrome extension will retrieve the data which the 'SHOULD_UPDATE' is True and update the database.                         
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
                    case "chat":
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
                                if f"{self.user.username}_chrome" in connected_users:
                                    print(f"connected_users - {connected_users}")
                                    is_sent = await self.channel_layer.send(
                                        connected_users[f"{self.user.username}_chrome"],
                                        {
                                            'type': 'send_message',
                                            'message': { "content": chat["content"], 'user': self.user.username }
                                        }
                                    )
                                    print(f"is_sent - {is_sent}")
                            else:
                                pass
                        else:
                            await self.send(text_data=json.dumps({'status': 'error', 'errors': "no prompt"}))
                        
                    case "chrome":
                        print(f"chrome - {data}")
                        await self.send(text_data=json.dumps({"type":"chrome", "action":"chat", 'message':"Chrome message received."}))
            case "chrome":
                print(f"chat - {data}")
                match data.get("action"):
                    case "update":
                        new_data = data.get("data")
                        print(f"Here is the updated data from Harverster Chrome Extension: {new_data}")
                        if f"{self.user.username}" in connected_users:
                            print(f"connected_users - {connected_users}")
                            await self.channel_layer.send(
                                connected_users[f"{self.user.username}"],
                                {
                                    'type': 'send_result',
                                    'message': { "content": f"Here is the updated data in json format from Harverster Chrome Extension: {new_data}.   Show me this data with good paragraph format. Summarize and format activities by each post subheading: Lots of columns - value/category/start date/schedule update etc ", 'user': f"{self.user.username}_chrome" }
                                }
                            )

    
    async def send_result(self, event):
        message = event['message']
        print(f"send_message - {message}") 
        print(self.interpreter)
        pass
        
        # try:
        msgs = []
        full_response = ""
        current_msg ={}
        for chunk in self.interpreter.chat(message["content"], stream=True, display=False):
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

        await self.save_messages(msgs)
        # Handler to receive the message and send it to the WebSocket
    async def send_message(self, event):
        message = event['message']
        print(f"send_message - {message}")
        profiles = await self.get_new_profile()
        # Send the message to the WebSocket client
        print(profiles)
        await self.send(text_data=json.dumps({
            'type': 'scrap',
            "data": profiles
        }))
        return True
    def create_user_folder(self, user):
        # Define the path to the user's folder
        user_dir = os.path.join(settings.BASE_DIR, 'static', user.username)

        # Check if the directory does not exist, then create it
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        return user_dir
    
    @database_sync_to_async
    def get_new_profile(self):
         
        ld_tz = pytz.timezone('Europe/London')

        # Get the current time in the specified timezone
        now = timezone.now().astimezone(ld_tz)


        # Define the time range (last 24 hours)
        time_threshold_london = now - timedelta(hours=2)
        time_threshold_utc = time_threshold_london.astimezone(pytz.utc)
        profiles = LinkedIn.objects.filter(url__isnull=True, last_updated__gte=time_threshold_utc)
        data = LinkedInSerializer(profiles, many=True).data
        print(data)
        return data
    
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