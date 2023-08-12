from django.contrib import admin
from .models import Airline, Aircraft, Airport, Flight

admin.site.register(Airline)
admin.site.register(Aircraft)
admin.site.register(Airport)
admin.site.register(Flight)
