from django_filters import rest_framework as filters
from .models import Contract


class ContractFilter(filters.FilterSet):
    date_created = filters.CharFilter(field_name='date_created', lookup_expr='icontains')
    amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    client_last_name = filters.CharFilter(field_name='client__last_name', lookup_expr='icontains')
    client_email = filters.CharFilter(field_name='client__email', lookup_expr='iexact')

    class Meta:
        model = Contract
        fields = ['date_created', 'amount', 'client']
