#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-10-11 17:18:09


import logging
from django.db.models import Q
from django.db.models.fields import DateTimeField, CharField, TextField
from django.db.models.fields.files import FileField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth import get_user_model
import django_filters


def create_filter(filters, model):
    if filters is not None:
        filter_name = "{}Filter".format(model.__name__.capitalize())
        if hasattr(filters, filter_name):
            return getattr(filters, filter_name)

    class Meta:
        fields = {}

    tmpMeta = Meta
    tmpMeta.model = model
    for field in model._meta.fields:
        if isinstance(field, FileField):
            continue
        elif isinstance(field, ForeignKey):
            related_model = field.related_model
            tmpMeta.fields[field.name] = ["exact"]
            for foreignkey_field in related_model._meta.fields:
                if isinstance(foreignkey_field, CharField):
                    new_field_name = "{}__{}".format(field.name, foreignkey_field.name)
                    tmpMeta.fields[new_field_name] = ["icontains", "exact"]
        elif isinstance(field, DateTimeField):
            tmpMeta.fields[field.name] = ["lte", "gte"]
        elif isinstance(field, TextField):
            tmpMeta.fields[field.name] = ["exact", "icontains"]
        elif isinstance(field, CharField):
            tmpMeta.fields[field.name] = ["exact", "icontains"]
        else:
            tmpMeta.fields[field.name] = ["exact"]
    tmpMeta.fields["keyword"] = []

    class ModelFilter(django_filters.rest_framework.FilterSet):
        keyword = django_filters.CharFilter(label="keyword", help_text="keyword关键词过滤", method="filter_keyword")

        Meta = tmpMeta

        def filter_keyword(self, queryset, name, value):
            q = Q()
            for field in queryset.model._meta.fields:
                if field.name == 'password':
                    continue
                if isinstance(field, CharField) or isinstance(field, TextField):
                    kwargs = {
                        "{}__icontains".format(field.name): value
                    }
                    q |= Q(**kwargs)
            # for field in queryset.model
            return queryset.filter(q)

    tmpFilter = ModelFilter
    return tmpFilter
