# Generated by Django 5.1.1 on 2024-10-24 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lo_profile', '0011_alter_contact_heading_alter_contact_project_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='last_checked_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
