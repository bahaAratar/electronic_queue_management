from django.contrib import admin
from .models import *

admin.site.register(Queue)
admin.site.register(Window)

# admin.site.register(Branches)