from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from .models import Event, EventStatus
from .filters import EventFilter
from accounts.models import Client
from .serializers import EventSerializer
from django.core.exceptions import ObjectDoesNotExist
from epicevents.utils import get_id_by_email
from epicevents.permissions import IsSales, IsSupport, IsManager


class EventViewset(ModelViewSet):
    # http_method_names = ['get', 'post', 'put']
    serializer_class = EventSerializer
    filter_class = EventFilter

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsManager | IsSales, ]
        elif self.action == 'list' or self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsManager | IsSales | IsSupport, ]
        elif self.action == 'destroy':
            permission_classes = [IsManager, ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.role == 'support_member':
            return Event.objects.filter(support_contact=self.request.user)
        elif self.request.user.role == 'sales_member':
            user_assigned_clients_ids = [client.id for client in Client.objects.filter(sales_contact=self.request.user)]
            return Event.objects.filter(client__in=user_assigned_clients_ids)
        elif self.request.user.role == 'management_member':
            return Event.objects.all().order_by("date_created")

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        try:
            request.POST['support_contact'] = get_id_by_email(request.POST['support_contact_email'])
            request.POST.pop('support_contact_email', None)
        except ValidationError:
            return Response({'support_contact_email': 'email does not exists.'})
        try:
            request.POST['client'] = get_id_by_email(request.POST['client_email'])
            request.POST.pop('client_email', None)
        except ValidationError:
            return Response({'client_email': 'email does not exists.'})
        request.POST['event_status'] = EventStatus.objects.get(event_status="created").id
        request.POST._mutable = False
        return super(EventViewset, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        try:
            request.POST['support_contact'] = get_id_by_email(request.POST['support_contact_email'])
            request.POST.pop('support_contact_email', None)
        except ValidationError:
            return Response({'support_contact_email': 'email does not exists.'})
        try:
            request.POST['client'] = get_id_by_email(request.POST['client_email'])
            request.POST.pop('client_email', None)
        except ValidationError:
            return Response({'client_email': 'email does not exists.'})
        try:
            request.POST['event_status'] = EventStatus.objects.get(event_status=request.POST['event_status']).id
        except ObjectDoesNotExist:
            return Response(
                {"event_status": "Not a valid status. Please enter one of these: 'created', 'in_pogress', 'finished'"})
        request.POST._mutable = False
        return super(EventViewset, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(EventViewset, self).destroy(request, *args, **kwargs)
