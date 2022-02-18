from django.contrib import admin
from .models import Contract


class ContractAdmin(admin.ModelAdmin):
    list_filter = ('date_created',)


admin.site.register(Contract, ContractAdmin)
