from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import fields
from .models import Event


class EventSerializer(ModelSerializer):
    event_date = fields.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])
    # client = SerializerMethodField()
    # support_contact = SerializerMethodField()
    #
    # def get_client(self, obj):
    #     return obj.client.email
    #
    # def get_support_contact(self, obj):
    #     return obj.sales_contact.email

    class Meta:
        model = Event
        fields = [
            'id',
            'support_contact',
            'client',
            'date_created',
            'date_updated',
            'event_status',
            'attendees',
            'event_date',
            'notes'
        ]





