from django.db.models.fields.files import FileField
from django.utils.decorators import classonlymethod
from functools import update_wrapper
import importlib
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from . import paginations, utils, mixins
from .serializers import MultiDeleteSerializer
from .filters import create_filter


class MyModelViewSet(mixins.AutoPermissionMixin, mixins.AutoSerializerMixin,
                     viewsets.ModelViewSet):
    model = None
    queryset = None
    pagination_class = paginations.PaginationClass
    permission_classes = []
    filters = None

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "filter_class"):
            self.filter_class = create_filter(self.filters, self.model)
        return super(MyModelViewSet, self).__init__(*args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def list(self, request, *args, **kwargs):
        logging.info("查看列表")
        logging.info(self.filter_class)
        return super(MyModelViewSet, self).list(request, *args, **kwargs)

    @classonlymethod
    def as_view(cls, actions=None, **initkwargs):
        """
        Because of the way class based views create a closure around the
        instantiated view, we need to totally reimplement `.as_view`,
        and slightly modify the view function that is created and returned.
        """
        # The name and description initkwargs may be explicitly overridden for
        # certain route configurations. eg, names of extra actions.
        cls.name = None
        cls.description = None

        # The suffix initkwarg is reserved for displaying the viewset type.
        # This initkwarg should have no effect if the name is provided.
        # eg. 'List' or 'Instance'.
        cls.suffix = None

        # The detail initkwarg is reserved for introspecting the viewset type.
        cls.detail = None

        # Setting a basename allows a view to reverse its action urls. This
        # value is provided by the router through the initkwargs.
        cls.basename = None

        # actions must not be empty
        if not actions:
            raise TypeError("The `actions` argument must be provided when "
                            "calling `.as_view()` on a ViewSet. For example "
                            "`.as_view({'get': 'list'})`")

        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that." %
                                (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r" %
                                (cls.__name__, key))

        # name and suffix are mutually exclusive
        if 'name' in initkwargs and 'suffix' in initkwargs:
            raise TypeError(
                "%s() received both `name` and `suffix`, which are "
                "mutually exclusive arguments." % (cls.__name__))

        def view(request, *args, **kwargs):
            """文档"""
            self = cls(**initkwargs)
            # We also store the mapping of request methods to actions,
            # so that we can later set the action attribute.
            # eg. `self.action = 'list'` on an incoming GET request.
            self.action_map = actions

            # Bind methods to actions
            # This is the bit that's different to a standard view
            for method, action in actions.items():
                handler = getattr(self, action)
                setattr(self, method, handler)

            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get

            self.request = request
            self.args = args
            self.kwargs = kwargs

            # And continue as usual
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        # class TmpClass(object):
        #     pass
        # tmpclass = TmpClass
        # tmpclass.__doc__ = "文档"
        # update_wrapper(view, tmpclass, updated=())
        # update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())

        # We need to set these on the view function, so that breadcrumb
        # generation can pick out these bits of information from a
        # resolved URL.
        view.cls = cls
        view.initkwargs = initkwargs
        view.actions = actions
        return csrf_exempt(view)

    def perform_create(self, serializer):
        kwargs = {}
        if hasattr(self.model, "user"):
            kwargs['user'] = self.request.user
            if self.request.user.is_authenticated is False:
                raise PermissionDenied("请先登录")
            if hasattr(self.model, "last_editor"):
                kwargs['last_editor'] = self.request.user
            instance = serializer.save(**kwargs)
            contenttype = ContentType.objects.get_for_model(self.model)
            LogEntry.objects.create(user=self.request.user,
                                    object_id=instance.id,
                                    object_repr=str(instance),
                                    content_type=contenttype,
                                    change_message=json.dumps([{
                                        'added': {}
                                    }]),
                                    action_flag=1)
        else:
            serializer.save()

    def get_filter_fields(self):
        filter_fields = []
        for field in self.model._meta.fields:
            if isinstance(field, FileField):
                continue
            filter_fields.append(field.name)
        return filter_fields

    def perform_destroy(self, instance):
        contenttype = ContentType.objects.get_for_model(self.model)
        LogEntry.objects.create(user=self.request.user,
                                object_id=instance.id,
                                object_repr=str(instance),
                                content_type=contenttype,
                                change_message="",
                                action_flag=3)
        instance.delete()

    def perform_update(self, serializer):
        if hasattr(self.model, "last_editor"):
            kwargs = {"last_editor": self.request.user}
        else:
            kwargs = {}
        instance = serializer.save(**kwargs)
        contenttype = ContentType.objects.get_for_model(self.model)
        LogEntry.objects.create(user=self.request.user,
                                object_id=instance.id,
                                object_repr=str(instance),
                                content_type=contenttype,
                                change_message="[]",
                                action_flag=2)
        return instance

    def update(self, request, *args, **kwargs):
        logging.info("update")
        model = self.model
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        for field in model._meta.get_fields():
            logging.info(field)
            if field.name not in request.data:
                continue
            else:
                logging.info(field)
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer_class = utils.RetrieveSerializerFactory(
            model).create_serializer()
        data = serializer_class(instance).data
        return Response(data)

    def create(self, request, *args, **kwargs):
        model = self.model
        for field in model._meta.get_fields():
            if field.name not in request.data:
                continue
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)


class MultiDeleteView(GenericAPIView):
    serializer_class = MultiDeleteSerializer

    def post(self, request, *args, **kwargs):
        """批量删除的接口"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.queryset.filter(id__in=serializer.validated_data["ids"]).delete()
        return Response(status=204)


class ModelViewSetFactory(object):
    def __init__(self, app_module, model, app_config=None):
        self.model = model
        self.app_module = app_module
        self.app_config = app_config

    def create_view_set(self):
        logging.info("create_view_set")

        class TmpModelViewSet(MyModelViewSet):
            pass

        model_view_set = TmpModelViewSet
        model_view_set.model = self.model
        model_view_set.queryset = self.model.objects.all()
        model_view_set.app_module = self.app_module
        model_view_set.app_config = self.app_config
        model_view_set.permissions = getattr(self.app_module, "permissions",
                                             None)
        model_view_set.serializers = getattr(self.app_module, "serializers",
                                             None)

        filter_class = create_filter(
            model_view_set.filters, model_view_set.model)
        print("开始找filters")
        print(self.app_config.name)
        if self.app_config.name == "money":
            import ipdb
            # ipdb.set_trace();
        if importlib.util.find_spec(
                "{}.filters".format(self.app_config.name)):
            print("has filters")
            filters = importlib.import_module(
                "{}.filters".format(self.app_config.name))
            filter_name = "{}Filter".format(self.model.__name__)
            if hasattr(filters, filter_name):
                filter_class = getattr(filters, filter_name)
                print("filter_class变了")
        model_view_set.filter_class = filter_class
        if self.app_config.name == "money":
            logging.info("money的filter_class是")
            logging.info(filter_class)
        return model_view_set


def get_list_create_api_view(model_class):
    class _ListCreateAPIView(ListCreateAPIView):

        ordering = ["id"]

        def get_queryset(self):
            return model_class.objects.all()

        def get_serializer_class(self):
            class Serializer(ModelSerializer):
                class Meta:
                    model = model_class
                    fields = "__all__"
            return Serializer
    return _ListCreateAPIView


def get_detail_api_view(model_class):
    class _RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

        ordering = ["id"]

        def get_queryset(self):
            return model_class.objects.all()

        def get_serializer_class(self):
            class Serializer(ModelSerializer):
                class Meta:
                    model = model_class
                    fields = "__all__"
            return Serializer

        def post(self, request, *args, **kwargs):
            return self.patch(request, *args, **kwargs)
    return _RetrieveUpdateDestroyAPIView
