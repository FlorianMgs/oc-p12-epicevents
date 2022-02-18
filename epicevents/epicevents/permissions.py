from rest_framework.permissions import BasePermission
from accounts.models import User, Client
from contracts.models import Contract
from events.models import Event


class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user and bool(request.user.groups.filter(name='management_members')):
            print('checked manager true')
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsSales(BasePermission):
    message = "You don't have permission to do that. Need to be Sales or Management member"

    def has_permission(self, request, view):
        if request.user and bool(request.user.groups.filter(name='sales_members')):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if type(obj) == Contract or type(obj) == Client or type(obj) == Event:
            if view.action in ['update', 'partial_update', 'retrieve', 'list']:
                return True
            if view.action == 'destroy':
                return False


class IsSupport(BasePermission):
    message = "You don't have permission to do that. Need to be Support or Management member"

    def has_permission(self, request, view):
        if request.user and bool(request.user.groups.filter(name='support_members')):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if type(obj) == Contract or type(obj) == Client:
            if view.action in ['retrieve', 'list']:
                return True
            if view.action in ['update', 'partial_update', 'destroy']:
                return False
        if type(obj) == Event:
            if view.action in ['update', 'partial_update', 'retrieve', 'list']:
                return True
            if view.action == 'destroy':
                return False
