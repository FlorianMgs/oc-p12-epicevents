from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction
from .filters import ContractFilter
from .models import Contract
from .serializers import ContractSerializer
from events.models import Event
from epicevents.utils import get_id_by_email
from epicevents.permissions import IsSales, IsSupport, IsManager


User = get_user_model()


class ContractViewset(ModelViewSet):
    serializer_class = ContractSerializer
    filter_class = ContractFilter

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsManager | IsSales, ]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsManager | IsSales | IsSupport, ]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsManager | IsSales, ]
        elif self.action == 'destroy':
            permission_classes = [IsManager, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.role == 'sales_member':
            return Contract.objects.filter(sales_contact=self.request.user).order_by("date_created")
        elif self.request.user.role == 'support_member':
            user_assigned_events_clients_ids = [event.client.id for event in Event.objects.filter(support_contact=self.request.user)]
            return Contract.objects.filter(client__in=user_assigned_events_clients_ids)
        elif self.request.user.role == 'management_member':
            return Contract.objects.all().order_by("date_created")

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        try:
            request.POST['sales_contact'] = get_id_by_email(request.POST['sales_contact_email'])
            request.POST.pop('sales_contact_email', None)
        except ValidationError:
            return Response({'sales_contact_email': 'email does not exists.'})
        try:
            request.POST['client'] = get_id_by_email(request.POST['client_email'])
            request.POST.pop('client_email', None)
        except ValidationError:
            return Response({'client_email': 'email does not exists.'})
        request.POST._mutable = False
        return super(ContractViewset, self).update(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        try:
            request.POST['sales_contact'] = get_id_by_email(request.POST['sales_contact_email'])
            request.POST.pop('sales_contact_email', None)
        except ValidationError:
            return Response({'sales_contact_email': 'email does not exists.'})
        try:
            request.POST['client'] = get_id_by_email(request.POST['client_email'])
            request.POST.pop('client_email', None)
        except ValidationError:
            return Response({'client_email': 'email does not exists.'})
        request.POST._mutable = False
        return super(ContractViewset, self).create(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        return super(ContractViewset, self).destroy(request, *args, **kwargs)
