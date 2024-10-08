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
    projectid = models.CharField(max_length=255)
    heading = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    addressline1 = models.CharField(max_length=255, blank=True, null=True)
    addressline2 = models.CharField(max_length=255, blank=True, null=True)
    addressline3 = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    borough = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    gov_region = models.CharField(max_length=255, blank=True, null=True)
    value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    valuetype = models.CharField(max_length=255, blank=True, null=True)
    planningstage = models.CharField(max_length=255, blank=True, null=True)
    contractstage = models.CharField(max_length=255, blank=True, null=True)
    startdate = models.DateField(blank=True, null=True)
    startdatetype = models.CharField(max_length=255, blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    enddatetype = models.CharField(max_length=255, blank=True, null=True)
    contractperiod = models.IntegerField(blank=True, null=True)
    dev_type = models.CharField(max_length=255, blank=True, null=True)
    project_size = models.CharField(max_length=255, blank=True, null=True)
    projectstatus = models.CharField(max_length=255, blank=True, null=True)
    site_area = models.DecimalField(max_digits=255, decimal_places=2, blank=True, null=True)
    floorarea = models.DecimalField(max_digits=255, decimal_places=2, blank=True, null=True)
    units = models.IntegerField(blank=True, null=True)
    storeys = models.IntegerField(blank=True, null=True)
    primarysectors = models.CharField(max_length=255, blank=True, null=True)
    primarycategory = models.CharField(max_length=255, blank=True, null=True)
    sector_group = models.CharField(max_length=255, blank=True, null=True)
    materials = models.TextField(blank=True, null=True)
    latestinformation = models.TextField(blank=True, null=True)
    schemedescription = models.TextField(blank=True, null=True)
    leadplanningapplicationnumber = models.CharField(max_length=255, blank=True, null=True)
    lead_application_submitted_date = models.DateField(blank=True, null=True)
    lead_application_decision_date = models.DateField(blank=True, null=True)
    decision = models.CharField(max_length=255, blank=True, null=True)
    councilname = models.CharField(max_length=255, blank=True, null=True)
    record_type = models.CharField(max_length=255, blank=True, null=True)
    
    role_name = models.CharField(max_length=255, blank=True, null=True)
    salutation = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    has_linkedin_url = models.BooleanField(default=False)
    linkedin_url = models.URLField(blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    personalemail = models.EmailField(blank=True, null=True)
    last_checked_date = models.DateField(blank=True, null=True)
    
    avatar = models.URLField(max_length=2083, blank=True, null=True)
    connections = models.CharField(max_length=255, blank=True, null=True)
    connect_level = models.CharField(max_length=255, blank=True, null=True)
    time_in_role = models.CharField(max_length=255, blank=True, null=True)
    activity = models.TextField(blank=True, null=True)

    office_name = models.CharField(max_length=255, blank=True, null=True)
    office_id = models.CharField(max_length=255, blank=True, null=True)
    addr_1 = models.CharField(max_length=255, blank=True, null=True)
    addr_2 = models.CharField(max_length=255, blank=True, null=True)
    addr_3 = models.CharField(max_length=255, blank=True, null=True)
    town_name = models.CharField(max_length=255, blank=True, null=True)
    county_name = models.CharField(max_length=255, blank=True, null=True)
    post_cd = models.CharField(max_length=255, blank=True, null=True)
    off_gov_region = models.CharField(max_length=255, blank=True, null=True)
    should_update = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.PROJECT_NAME