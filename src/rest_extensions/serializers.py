#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-10-11 11:59:22


import json
from rest_framework import serializers


class MyJSONField(serializers.Field):
    default_error_messages = {
        'invalid': 'Value must be valid JSON.'
    }

    def to_internal_value(self, data):
        if not data:
            return data
        if isinstance(data, dict):
            return json.dumps(
                data, indent=4, ensure_ascii=False, sort_keys=True)
        elif isinstance(data, list):
            return json.dumps(
                data, indent=4, ensure_ascii=False, sort_keys=True)
        else:
            self.fail('invalid')

    def to_representation(self, value):
        try:
            return json.loads(value)
        except:
            return value


class MultiDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), help_text="要删除的id列表")

    class Meta:
        fields = ["ids"]


class MultiActionSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), help_text="要操作的id列表")

    class Meta:
        fields = ["ids"]
