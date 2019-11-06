#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2019-10-10 22:28:41


import django_filters
from rest_framework import serializers
from django.db.models.fields.related import ManyToManyField
from rest_extensions.fields import DataListField
from rest_extensions.serializers import MyJSONField


class CreateSerializerFactory(object):
    def __init__(self, model):
        self.all_fields = model._meta.get_fields()
        self.simple_field = model._meta.fields
        self.model = model

        class Serializer(serializers.ModelSerializer):
            class Meta:
                fields = []

            def create(self, validated_data):
                poped_many_fields = {}  # {"name": [1,2,3] }
                instance = self.Meta.model.objects.create(**validated_data)
                for field_name, values in poped_many_fields.items():
                    getattr(instance, field_name).set(values)
                    instance.save()
                return instance

        self.serializer_class = Serializer
        self.serializer_class.Meta.model = self.model
        self.serializer_class.serializer_field_mapping[
            DataListField] = MyJSONField

    def create_serializer(self):
        for field in self.all_fields:
            if field in self.simple_field:
                self.serializer_class.Meta.fields.append(field.name)
            elif isinstance(field, ManyToManyField):
                _ = serializers.PrimaryKeyRelatedField(
                    queryset=field.related_model.objects.all(), many=True)
                setattr(self.serializer_class, field.name, _)
                self.serializer_class.Meta.fields.append(field.name)
        return self.serializer_class


class ListSerializerFactory(object):
    def __init__(self, model):
        self.all_fields = model._meta.get_fields()
        self.simple_field = model._meta.fields
        self.model = model

        class Serializer(serializers.ModelSerializer):
            class Meta:
                fields = []

            def create(self, validated_data):
                poped_many_fields = {}  # {"name": [1,2,3] }
                instance = self.Meta.model.objects.create(**validated_data)
                for field_name, values in poped_many_fields.items():
                    getattr(instance, field_name).set(values)
                    instance.save()
                return instance

        self.serializer_class = Serializer
        self.serializer_class.Meta.model = self.model
        self.serializer_class.serializer_field_mapping[
            DataListField] = MyJSONField

    def create_serializer(self):
        for field in self.all_fields:
            if field in self.simple_field:
                self.serializer_class.Meta.fields.append(field.name)
        return self.serializer_class


class RetrieveSerializerFactory(object):
    def __init__(self, model):
        self.all_fields = model._meta.get_fields()
        self.simple_field = model._meta.fields
        self.model = model

        class Serializer(serializers.ModelSerializer):
            class Meta:
                fields = []
                depth = 2

        self.serializer_class = Serializer
        self.serializer_class.Meta.model = self.model
        self.serializer_class.serializer_field_mapping[
            DataListField] = MyJSONField

    def create_serializer(self):
        for field in self.simple_field:
            self.serializer_class.Meta.fields.append(field.name)
        return self.serializer_class


class UpdateSerializerFactory(object):
    def __init__(self, model):
        self.all_fields = model._meta.get_fields()
        self.simple_field = model._meta.fields
        self.model = model

        class Serializer(serializers.ModelSerializer):
            class Meta:
                fields = []

            def update(self, instance, validated_data):
                all_fields = self.Meta.model._meta.get_fields()
                simple_field = self.Meta.model._meta.fields
                poped_many_fields = {}  # {"name": [1,2,3] }
                for field in all_fields:
                    if field in simple_field:
                        continue
                    elif isinstance(field, ManyToManyField):
                        if field.name not in validated_data:
                            continue
                        else:
                            poped_many_fields[field.name] = validated_data.pop(
                                field.name)
                for field_name, values in poped_many_fields.items():
                    getattr(instance, field_name).set(values)
                    instance.save()
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                return instance

        self.serializer_class = Serializer
        self.serializer_class.Meta.model = self.model
        self.serializer_class.serializer_field_mapping[
            DataListField] = MyJSONField

    def create_serializer(self):
        for field in self.all_fields:
            if field.name == "user":
                continue
            elif field in self.simple_field:
                self.serializer_class.Meta.fields.append(field.name)
            elif isinstance(field, ManyToManyField):
                _ = serializers.PrimaryKeyRelatedField(
                    queryset=field.related_model.objects.all(), many=True)
                setattr(self.serializer_class, field.name, _)
                self.serializer_class.Meta.fields.append(field.name)
        return self.serializer_class


class FilterClassFactory(object):
    def __init__(self, model):
        self.all_fields = model._meta.get_fields()
        self.simple_field = model._meta.fields
        self.model = model

        class FilterClass(django_filters.rest_framework.FilterSet):
            class Meta:
                fields = ["id"]

        self.filter_class = FilterClass
        self.filter_class.Meta.model = self.model

    def create_filter_class(self):
        for field in self.all_fields:
            self.filter_class.Meta.fields.append(field.name)
        return self.filter_class


def document_tuple(choices):
    return "; ".join(map(lambda x: u"%s:%s" % (x[0], x[1]), choices))
