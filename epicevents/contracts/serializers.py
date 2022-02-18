from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import fields
from accounts.models import Client, User
from .models import Contract


class ContractSerializer(ModelSerializer):
    payment_due = fields.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

    # client = SerializerMethodField()
    # sales_contact = SerializerMethodField()
    #
    # def get_client(self, obj):
    #     return obj.client.email
    #
    # def get_sales_contact(self, obj):
    #     return obj.sales_contact.email

    class Meta:
        model = Contract
        fields = [
            'id',
            'sales_contact',
            'client',
            'date_created',
            'date_updated',
            'status',
            'amount',
            'payment_due'
        ]

