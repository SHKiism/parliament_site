from django.contrib import admin

from accounts.models import Citizen, Employee

# Register your models here.
admin.site.register(Citizen)
admin.site.register(Employee)