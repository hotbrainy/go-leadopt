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

from asgiref.sync import sync_to_async

from channels.db import database_sync_to_async 
from channels.generic.websocket import AsyncWebsocketConsumer 

# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser

from interpreter import OpenInterpreter, AsyncInterpreter

from . import models
from .serializers import ChatSerializer, MessageSerializer, SessionSerializer
from lo_profile.models import LinkedIn, Contact
from lo_profile.serializers import LinkedInSerializer, ContactSerializer

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
                        When you connect to the database, please don't show the credentials in the chat. And don't store the credentials in the chat.
                        And don't forget to close the connection after you finish your work.
                        In the database which you will connect to automatically, the list called `lo_profile_contact` is composed of contacts and leads. if asked for contacts and leads you will assume `lo_profile_contact` is where they are stored. the database is made up of people at construction companies. where as an an example the materials column lists the materials used, you will have an in-depth understanding of services that they will require to complete their development. 
                        At the start, get all data from the database - you need to connect to database in the background and get all data from the collection `lo_profile_contact`.
                        All field names are in lowercase. 
                        Here’s a simplified breakdown of the fields, assuming they're for managing construction projects:

                            projectid: Unique identifier for the project.
                            heading: Short title or description of the project.
                            project_name: The full name of the project.
                            addressline1, addressline2, addressline3: Lines for the project’s address, broken down for detailed formatting.
                            town, borough, county: The town, borough, and county where the project is located.
                            postcode: Postal code of the project site.
                            gov_region: Government region where the project is located.
                            value: The monetary value of the project.
                            valuetype: Type of value (e.g., estimated, contract value).
                            planningstage: Current stage in the planning process.
                            contractstage: Current stage in the contracting process.
                            startdate, startdatetype: Project start date and type (e.g., estimated or confirmed).
                            enddate, enddatetype: Project end date and type (e.g., estimated or confirmed).
                            contractperiod: Duration of the contract (e.g., in months).
                            dev_type: Type of development (e.g., residential, commercial).
                            project_size: The size of the project (could refer to cost, scale, or area).
                            projectstatus: Current status (e.g., in progress, completed).
                            site_area: Total area of the project site.
                            floorarea: Total floor area being constructed.
                            units: Number of units (e.g., apartments).
                            storeys: Number of storeys/floors in the project.
                            primarysectors: The main sectors involved (e.g., housing, infrastructure).
                            primarycategory: Main category of the project (e.g., construction, refurbishment).
                            sector_group: Group to which the sector belongs (e.g., private or public).
                            materials: Key materials used in the project (e.g., concrete, steel).
                            latestinformation: The most recent updates or changes in the project.
                            schemedescription: Detailed description of the project plan or scheme.
                            leadplanningapplicationnumber: Reference number for the main planning application.
                            lead_application_submitted_date: Date the lead planning application was submitted.
                            lead_application_decision_date: Date a decision was made on the application.
                            decision: Outcome of the planning application (e.g., approved, rejected).
                            councilname: Name of the council responsible for the project.
                            record_type: Type of record (e.g., planning, construction).
                            role_name: The role of the contact person (e.g., architect, project manager).
                            salutation, first_name, last_name: Contact person’s title (e.g., Mr., Ms.), first and last name.
                            has_linkedin_url: Indicates whether the contact has a LinkedIn profile (True/False).
                            linkedin_url: The LinkedIn profile URL of the contact.
                            job_title: Job title of the contact.
                            phone: Contact’s office phone number.
                            mobile: Contact’s mobile phone number.
                            personalemail: Contact’s personal email.
                            last_checked_date: Last date the contact information was updated.
                            office_name: Name of the office responsible for the project.
                            office_id: Unique identifier for the office.
                            addr_1, addr_2, addr_3: Address lines for the office.
                            town_name, county_name, post_cd: Town, county, and postal code for the office.
                            off_gov_region: Government region where the office is located.
                            should_update: Indicates whether the contact information needs to be updated by harvester.(True/False)
                        # STYLE
                        All answers will be given in as few words as possible. don't say "i'll update the code" or "i'll write a function" - just do it.
                        I need the very precise and concise answer as less as possible.
                        Don't use any greetings or sign-offs.
                        Don't describe any steps or processes.
                        Don't explain any code or concepts.
                        Just do the task as quickly as possible.
                        And return the answer in the simplest form.
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
                        If you are asked to ask harvester to update the data, you will update the field 'should_update' with boolean value True.
                        If you are asked to update contact data you automatically know that you just update the field 'should_update' with boolean value True.
                        e.g. with linkedin, you are not capable of updating information using linkedin, you can update the field 'should_update' with boolean value True and this will send you the data to update the database. it is very important you do not try and access linkedin to update the data and instead just update the field 'should_update' with boolean value True. You will report "I've asked Harvester to update the data".
                        if you are asked to the data again, you need to re run the query to get the updated data.
                        
                        # TASK
                        Add mentioned “Names” + “LinkedinUrls” (e.g. Andrew Ward > href=andrew ward’s linkedinurl)
                        Format activities by each post subheading: Lots of columns - value/category/start date/schedule update etc.                 
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
        profiles = await self.get_should_be_updated_contact()
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
    def get_should_be_updated_contact(self):
          
 
        contacts = Contact.objects.filter(should_update=True)
        data = ContactSerializer(contacts, many=True).data
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