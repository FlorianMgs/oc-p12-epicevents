from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    event_date = filters.CharFilter(field_name='event_date', lookup_expr='icontains')
    client_last_name = filters.CharFilter(field_name='client__last_name', lookup_expr='icontains')
    client_email = filters.CharFilter(field_name='client__email', lookup_expr='iexact')

    class Meta:
        model = Event
        fields = ['event_date', 'client']
