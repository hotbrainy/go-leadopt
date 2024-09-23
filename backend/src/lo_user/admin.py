from django.contrib import admin

# Register your models here.
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('first_name',"last_name",'avatar', "username","id","email","password","is_superuser", "date_joined", "is_active")