from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class LinkedIn(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(max_length=2083, blank=True, null=True)
    avatar = models.URLField(max_length=2083, blank=True, null=True)
    connections = models.CharField(max_length=255, blank=True, null=True)
    connect_level = models.CharField(max_length=255, blank=True, null=True)
    time_in_role = models.CharField(max_length=255, blank=True, null=True)
    activity = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    

class Contact(models.Model):    
    id = models.AutoField(primary_key=True)
    PROJECTID = models.CharField(max_length=255)
    HEADING = models.CharField(max_length=255)
    PROJECT_NAME = models.CharField(max_length=255)
    ADDRESSLINE1 = models.CharField(max_length=255, blank=True, null=True)
    ADDRESSLINE2 = models.CharField(max_length=255, blank=True, null=True)
    ADDRESSLINE3 = models.CharField(max_length=255, blank=True, null=True)
    TOWN = models.CharField(max_length=255, blank=True, null=True)
    BOROUGH = models.CharField(max_length=255, blank=True, null=True)
    COUNTY = models.CharField(max_length=255, blank=True, null=True)
    POSTCODE = models.CharField(max_length=255, blank=True, null=True)
    GOV_REGION = models.CharField(max_length=255, blank=True, null=True)
    VALUE = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    VALUETYPE = models.CharField(max_length=255, blank=True, null=True)
    PLANNINGSTAGE = models.CharField(max_length=255, blank=True, null=True)
    CONTRACTSTAGE = models.CharField(max_length=255, blank=True, null=True)
    STARTDATE = models.DateField(blank=True, null=True)
    STARTDATETYPE = models.CharField(max_length=255, blank=True, null=True)
    ENDDATE = models.DateField(blank=True, null=True)
    ENDDATETYPE = models.CharField(max_length=255, blank=True, null=True)
    CONTRACTPERIOD = models.IntegerField(blank=True, null=True)
    DEV_TYPE = models.CharField(max_length=255, blank=True, null=True)
    PROJECT_SIZE = models.CharField(max_length=255, blank=True, null=True)
    PROJECTSTATUS = models.CharField(max_length=255, blank=True, null=True)
    SITE_AREA = models.DecimalField(max_digits=255, decimal_places=2, blank=True, null=True)
    FLOORAREA = models.DecimalField(max_digits=255, decimal_places=2, blank=True, null=True)
    UNITS = models.IntegerField(blank=True, null=True)
    STOREYS = models.IntegerField(blank=True, null=True)
    PRIMARYSECTORS = models.CharField(max_length=255, blank=True, null=True)
    PRIMARYCATEGORY = models.CharField(max_length=255, blank=True, null=True)
    SECTOR_GROUP = models.CharField(max_length=255, blank=True, null=True)
    MATERIALS = models.TextField(blank=True, null=True)
    LATESTINFORMATION = models.TextField(blank=True, null=True)
    SCHEMEDESCRIPTION = models.TextField(blank=True, null=True)
    LEADPLANNINGAPPLICATIONNUMBER = models.CharField(max_length=255, blank=True, null=True)
    LEAD_APPLICATION_SUBMITTED_DATE = models.DateField(blank=True, null=True)
    LEAD_APPLICATION_DECISION_DATE = models.DateField(blank=True, null=True)
    DECISION = models.CharField(max_length=255, blank=True, null=True)
    COUNCILNAME = models.CharField(max_length=255, blank=True, null=True)
    RECORD_TYPE = models.CharField(max_length=255, blank=True, null=True)
    
    ROLE_NAME = models.CharField(max_length=255, blank=True, null=True)
    SALUTATION = models.CharField(max_length=255, blank=True, null=True)
    FIRST_NAME = models.CharField(max_length=255, blank=True, null=True)
    LAST_NAME = models.CharField(max_length=255, blank=True, null=True)
    HAS_LINKEDIN_URL = models.BooleanField(default=False)
    LINKEDIN_URL = models.URLField(blank=True, null=True)
    JOB_TITLE = models.CharField(max_length=255, blank=True, null=True)
    PHONE = models.CharField(max_length=255, blank=True, null=True)
    MOBILE = models.CharField(max_length=255, blank=True, null=True)
    PERSONALEMAIL = models.EmailField(blank=True, null=True)
    LAST_CHECKED_DATE = models.DateField(blank=True, null=True)
    
    OFFICE_NAME = models.CharField(max_length=255, blank=True, null=True)
    OFFICE_ID = models.CharField(max_length=255, blank=True, null=True)
    ADDR_1 = models.CharField(max_length=255, blank=True, null=True)
    ADDR_2 = models.CharField(max_length=255, blank=True, null=True)
    ADDR_3 = models.CharField(max_length=255, blank=True, null=True)
    TOWN_NAME = models.CharField(max_length=255, blank=True, null=True)
    COUNTY_NAME = models.CharField(max_length=255, blank=True, null=True)
    POST_CD = models.CharField(max_length=255, blank=True, null=True)
    OFF_GOV_REGION = models.CharField(max_length=255, blank=True, null=True)
    SHOULD_UPDATE = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.PROJECT_NAME