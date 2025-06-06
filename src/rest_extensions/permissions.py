#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2019-10-10 01:13:52


from rest_framework.permissions import BasePermission


class NoDeletePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == "DELETE":
            return False
        return True


class SelfPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
