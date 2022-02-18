from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from accounts.models import Client
from events.models import Event
from epicevents.utils import get_id_by_email
from .filters import ClientFilter
from .serializers import UserSignupSerializer, ClientSerializer
from epicevents.permissions import IsSales, IsSupport, IsManager


User = get_user_model()


class SignupViewset(APIView):

    permission_classes = (IsManager, )

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.role == 'sales_member':
                group = Group.objects.get(name='sales_members')
            elif user.role == 'support_member':
                group = Group.objects.get(name='support_members')
            else:
                group = Group.objects.get(name='management_members')
            user.groups.add(group)
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ClientViewset(ModelViewSet):
    serializer_class = ClientSerializer
    filter_class = ClientFilter

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
            return Client.objects.filter(sales_contact=self.request.user).order_by("date_created")
        elif self.request.user.role == 'support_member':
            user_assigned_events_clients_ids = [event.client.id for event in Event.objects.filter(support_contact=self.request.user)]
            return Client.objects.filter(id__in=user_assigned_events_clients_ids)
        elif self.request.user.role == 'management_member':
            return Client.objects.all().order_by("date_created")

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        try:
            request.POST['sales_contact'] = get_id_by_email(request.POST['sales_contact_email'])
            request.POST.pop('sales_contact_email', None)
        except ValidationError:
            return Response({'sales_contact_email': 'email does not exists.'})
        request.POST._mutable = False
        return super(ClientViewset, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        try:
            request.POST['sales_contact'] = get_id_by_email(request.POST['sales_contact_email'])
            request.POST.pop('sales_contact_email', None)
        except ValidationError:
            return Response({'sales_contact_email': 'email does not exists.'})
        request.POST._mutable = False
        return super(ClientViewset, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(ClientViewset, self).destroy(request, *args, **kwargs)
