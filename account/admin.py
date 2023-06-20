from django.contrib import admin
from .models import CustomUser

class Admin(admin.ModelAdmin):
    list_display = ('email', 'phone_number',)

admin.site.register(CustomUser, Admin)
