from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib import admin
from .models import User, Client
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', )


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_filter = ('role', )
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    list_display = ('id', 'email', )
    ordering = ('email',)


admin.site.register(User, UserAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_filter = ('email', 'last_name', 'date_created')


admin.site.register(Client, ClientAdmin)
