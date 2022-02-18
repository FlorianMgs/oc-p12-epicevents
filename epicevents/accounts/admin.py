from django.contrib import admin
from .models import User, Client


class UserAdmin(admin.ModelAdmin):
    list_filter = ('role', )


admin.site.register(User, UserAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_filter = ('email', 'last_name', 'date_created')


admin.site.register(Client, ClientAdmin)
