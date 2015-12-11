#!usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """
    List : admin only
    Create : anyone
    Retrieve : own self or admin
    Update : own self or admin
    Partial update : own self or admin
    Destroy : admin only
    """
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated() and request.user.is_admin
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return request.user.is_authenticated() and (obj == request.user or request.user.is_admin)
        elif view.action in ['update', 'partial_update']:
            return request.user.is_authenticated() and (obj == request.user or request.user.is_admin)
        elif view.action == 'destroy':
            return request.user.is_authenticated() and request.user.is_admin
        else:
            return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Read : anyone
    Delete : admin only
    Create, Update : author only
    """
    def has_object_permission(self, request, view, obj):
        # Anyone can read (HTTP method : GET, HEAD, and OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only admin can delete (HTTP method : DELETE)
        if request.method == 'DELETE':
            return request.user.is_admin
        
        # Only author can create and update (HTTP method : POST, PUT, PATCH)
        return obj.author == request.user
