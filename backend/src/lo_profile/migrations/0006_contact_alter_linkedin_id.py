# Generated by Django 5.1.1 on 2024-09-29 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lo_profile', '0005_alter_linkedin_avatar_alter_linkedin_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('PROJECTID', models.CharField(max_length=255)),
                ('HEADING', models.CharField(max_length=255)),
                ('PROJECT_NAME', models.CharField(max_length=255)),
                ('ADDRESSLINE1', models.CharField(blank=True, max_length=255, null=True)),
                ('ADDRESSLINE2', models.CharField(blank=True, max_length=255, null=True)),
                ('ADDRESSLINE3', models.CharField(blank=True, max_length=255, null=True)),
                ('TOWN', models.CharField(blank=True, max_length=255, null=True)),
                ('BOROUGH', models.CharField(blank=True, max_length=255, null=True)),
                ('COUNTY', models.CharField(blank=True, max_length=255, null=True)),
                ('POSTCODE', models.CharField(blank=True, max_length=10, null=True)),
                ('GOV_REGION', models.CharField(blank=True, max_length=255, null=True)),
                ('VALUE', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('VALUETYPE', models.CharField(blank=True, max_length=255, null=True)),
                ('PLANNINGSTAGE', models.CharField(blank=True, max_length=255, null=True)),
                ('CONTRACTSTAGE', models.CharField(blank=True, max_length=255, null=True)),
                ('STARTDATE', models.DateField(blank=True, null=True)),
                ('STARTDATETYPE', models.CharField(blank=True, max_length=255, null=True)),
                ('ENDDATE', models.DateField(blank=True, null=True)),
                ('ENDDATETYPE', models.CharField(blank=True, max_length=255, null=True)),
                ('CONTRACTPERIOD', models.IntegerField(blank=True, null=True)),
                ('DEV_TYPE', models.CharField(blank=True, max_length=255, null=True)),
                ('PROJECT_SIZE', models.CharField(blank=True, max_length=255, null=True)),
                ('PROJECTSTATUS', models.CharField(blank=True, max_length=255, null=True)),
                ('SITE_AREA', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('FLOORAREA', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('UNITS', models.IntegerField(blank=True, null=True)),
                ('STOREYS', models.IntegerField(blank=True, null=True)),
                ('PRIMARYSECTORS', models.CharField(blank=True, max_length=255, null=True)),
                ('PRIMARYCATEGORY', models.CharField(blank=True, max_length=255, null=True)),
                ('SECTOR_GROUP', models.CharField(blank=True, max_length=255, null=True)),
                ('MATERIALS', models.TextField(blank=True, null=True)),
                ('LATESTINFORMATION', models.TextField(blank=True, null=True)),
                ('SCHEMEDESCRIPTION', models.TextField(blank=True, null=True)),
                ('LEADPLANNINGAPPLICATIONNUMBER', models.CharField(blank=True, max_length=255, null=True)),
                ('LEAD_APPLICATION_SUBMITTED_DATE', models.DateField(blank=True, null=True)),
                ('LEAD_APPLICATION_DECISION_DATE', models.DateField(blank=True, null=True)),
                ('DECISION', models.CharField(blank=True, max_length=255, null=True)),
                ('COUNCILNAME', models.CharField(blank=True, max_length=255, null=True)),
                ('RECORD_TYPE', models.CharField(blank=True, max_length=255, null=True)),
                ('ROLE_NAME', models.CharField(blank=True, max_length=255, null=True)),
                ('SALUTATION', models.CharField(blank=True, max_length=10, null=True)),
                ('FIRST_NAME', models.CharField(blank=True, max_length=255, null=True)),
                ('LAST_NAME', models.CharField(blank=True, max_length=255, null=True)),
                ('CONTACT', models.CharField(blank=True, max_length=255, null=True)),
                ('HAS_LINKEDIN_URL', models.BooleanField(default=False)),
                ('CONTACT_LINKEDIN_URL', models.URLField(blank=True, null=True)),
                ('CONTACT_ID', models.CharField(blank=True, max_length=255, null=True)),
                ('JOB_TITLE', models.CharField(blank=True, max_length=255, null=True)),
                ('CONTACT_PHONE', models.CharField(blank=True, max_length=20, null=True)),
                ('CONTACT_MOBILE', models.CharField(blank=True, max_length=20, null=True)),
                ('PERSONALEMAIL', models.EmailField(blank=True, max_length=254, null=True)),
                ('LAST_CHECKED_DATE', models.DateField(blank=True, null=True)),
                ('OFFICE_NAME', models.CharField(blank=True, max_length=255, null=True)),
                ('OFFICE_ID', models.CharField(blank=True, max_length=255, null=True)),
                ('ADDR_1', models.CharField(blank=True, max_length=255, null=True)),
                ('ADDR_2', models.CharField(blank=True, max_length=255, null=True)),
                ('ADDR_3', models.CharField(blank=True, max_length=255, null=True)),
                ('TOWN_NAME', models.CharField(blank=True, max_length=255, null=True)),
                ('COUNTY_NAME', models.CharField(blank=True, max_length=255, null=True)),
                ('POST_CD', models.CharField(blank=True, max_length=10, null=True)),
                ('OFF_GOV_REGION', models.CharField(blank=True, max_length=255, null=True)),
                ('PHONE', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='linkedin',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
