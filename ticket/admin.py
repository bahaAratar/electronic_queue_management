from django.contrib import admin
from .models import *

admin.site.register(Ticket)
admin.site.register(Region)
admin.site.register(Area)
admin.site.register(City)
admin.site.register(Department)