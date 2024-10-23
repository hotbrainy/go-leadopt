from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers 
from .models import LinkedIn, Contact
# User = get_user_model()

class LinkedInSerializer(serializers.HyperlinkedModelSerializer):
    # id = serializers.IntegerField()
    class Meta:
        model = LinkedIn
        fields = "__all__"

class ContactSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    class Meta:
        model = Contact
        fields = "__all__"
        #     "projectid", 
        #     "heading", 
        #     "project_name", 
        #     "addressline1", 
        #     "addressline2", 
        #     "addressline3", 
        #     "town", 
        #     "borough", 
        #     "county", 
        #     "postcode", 
        #     "gov_region", 
        #     "value", 
        #     "valuetype", 
        #     "planningstage", 
        #     "contractstage", 
        #     "startdate", 
        #     "startdatetype", 
        #     "enddate", 
        #     "enddatetype", 
        #     "contractperiod", 
        #     "dev_type", 
        #     "project_size", 
        #     "projectstatus", 
        #     "site_area", 
        #     "floorarea", 
        #     "units", 
        #     "storeys", 
        #     "primarysectors", 
        #     "primarycategory", 
        #     "sector_group", 
        #     "materials", 
        #     "latestinformation", 
        #     "schemedescription", 
        #     "leadplanningapplicationnumber", 
        #     "lead_application_submitted_date", 
        #     "lead_application_decision_date", 
        #     "decision", 
        #     "councilname", 
        #     "record_type",  
        #     "role_name", 
        #     "salutation", 
        #     "first_name", 
        #     "last_name", 
        #     "has_linkedin_url", 
        #     "linkedin_url", 
        #     "job_title", 
        #     "phone", 
        #     "mobile", 
        #     "personalemail", 
        #     "last_checked_date", 
        #     "avatar", 
        #     "connections", 
        #     "connect_level", 
        #     "time_in_role", 
        #     "activity", 
        #     "office_name", 
        #     "office_id", 
        #     "addr_1", 
        #     "addr_2", 
        #     "addr_3", 
        #     "town_name", 
        #     "county_name", 
        #     "post_cd", 
        #     "off_gov_region", 
        #     "should_update", 
        # ]