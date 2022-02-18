from django.contrib import admin
from .models import Event, EventStatus


class EventAdmin(admin.ModelAdmin):
    list_filter = ('event_status__event_status', 'date_created')


admin.site.register(Event, EventAdmin)
admin.site.register(EventStatus)
