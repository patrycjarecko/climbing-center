from django.contrib.auth.models import Group
from rest_framework import permissions

class IsAdministratorUser(permissions.BasePermission):
    #nie wiem czy sie przyda
    '''def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user.role'''

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Administrator'


class IsInstructorUser(permissions.BasePermission):
    #nie wiem czy sie przyda
    '''def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user.role'''

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Instructor'


class IsReceptionistUser(permissions.BasePermission):
    #nie wiem czy sie przyda
    '''def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user.role'''

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Receptionist'