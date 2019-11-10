import logging
import importlib
from rest_framework import serializers as rest_serializers
from rest_extensions.fields import DataListField
from rest_extensions.serializers import MyJSONField
from . import utils


class AutoSerializerMixin(object):
    def get_serializer_class(self):
        logging.info("get serializers")
        serializers = None
        if getattr(self, "serializers", None):
            logging.info("has serializers")
            serializers = self.serializers
        elif getattr(self, "app_module", None):
            logging.info("has app_module")
            if importlib.util.find_spec(
                    "{}.serializers".format(self.app_config.name)):
                serializers = importlib.import_module(
                    "{}.serializers".format(self.app_config.name))
        serializer_name1 = "{model_name}{action}Serializer".format(
            model_name=self.model.__name__,
            action=self.action.capitalize(),
        )
        serializer_name2 = "{model_name}Serializer".format(
            model_name=self.model.__name__, )
        serializer_name3 = "{model_name}BaseSerializer".format(
            model_name=self.model.__name__, )
        for name in [serializer_name1, serializer_name2, serializer_name3]:
            serializer_class = getattr(serializers, name, None)
            if serializer_class:
                return serializer_class
        logging.info("{} Does not exist".format(serializer_name1, serializer_name2, serializer_name3))

        if self.action == "create":
            return utils.CreateSerializerFactory(
                self.model).create_serializer()
        elif self.action == "list":
            return utils.ListSerializerFactory(
                self.model).create_serializer()
        elif "update" in self.action:
            return utils.UpdateSerializerFactory(
                self.model).create_serializer()

        class Meta:
            fields = "__all__"
            depth = 0
            model = self.model

        tmpMeta = Meta

        class TmpSerializer(rest_serializers.ModelSerializer):
            Meta = tmpMeta

        serializer_class = TmpSerializer
        serializer_class.serializer_field_mapping[DataListField] = MyJSONField
        return serializer_class


class AutoPermissionMixin(object):
    def get_permissions(self):
        logging.info("AutoPermissionMixin.get_permissions")
        permissions = [permission() for permission in self.permission_classes]
        if self.permissions is not None:
            permission_class_name = "{model_name}Permission".format(
                model_name=self.model.__name__)
            if hasattr(self.permissions, permission_class_name):
                permissions.append(
                    getattr(self.permissions, permission_class_name)()
                )
        else:
            logging.info("no permissions file")
        return permissions
