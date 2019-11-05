from django.shortcuts import render
from django.db.models.fields.files import FileField
from django.utils.decorators import classonlymethod
from functools import update_wrapper
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.models import LogEntry
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related import ManyToManyField
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_extensions.fields import DataListField
from rest_extensions.serializers import MyJSONField
from . import paginations, permissions, utils, mixins
from .serializers import MultiDeleteSerializer
from .filters import create_filter
import django_filters


class AutoSerializerMixin(object):
    def get_serializer_class(self):
        serializer_name1 = "{model_name}{action}Serializer".format(
            model_name=self.model.__name__,
            action=self.action.capitalize(),
        )
        serializer_name2 = "{model_name}Serializer".format(
            model_name=self.model.__name__, )
        serializer_name3 = "{model_name}BaseSerializer".format(
            model_name=self.model.__name__, )
        for name in [serializer_name1, serializer_name2, serializer_name3]:
            serializer_class = getattr(self.serializers, name, None)
            if serializer_class:
                return serializer_class

        if self.action == "create":
            return utils.CreateSerializerFactory(
                self.model).create_serializer()
        elif "update" in self.action:
            return utils.UpdateSerializerFactory(
                self.model).create_serializer()

        class Meta:
            fields = "__all__"
            depth = 2
            model = self.model

        tmpMeta = Meta

        class TmpSerializer(serializers.ModelSerializer):
            Meta = tmpMeta

            def to_representation(self, obj):
                data = super(TmpSerializer, self).to_representation(obj)
                if "user" in data:
                    for key in ["password", "groups", "user_permissions"]:
                        if key in data["user"]:
                            data["user"].pop(key)
                if hasattr(obj, "display_name"):
                    data["display_name"] = obj.display_name
                return data

        serializer_class = TmpSerializer
        # logging.info(self.model)
        # breakpoint()
        serializer_class.serializer_field_mapping[DataListField] = MyJSONField
        return serializer_class


class AutoPermissionMixin(object):
    def get_permissions(self):
        logging.info("AutoPermissionMixin.get_permissions")
        permissions = [permission() for permission in self.permission_classes]
        if self.permissions is not None:
            permission_class_name = "{model_name}Permission".format(model_name=self.model.__name__)
            if hasattr(self.permissions, permission_class_name):
                permissions.append(
                    getattr(self.permissions, permission_class_name)()
                )
            else:
                logging.info("没有权限")
        else:
            logging.info("都没有传入permissions")
        return permissions
