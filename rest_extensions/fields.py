#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-10-17 09:31:03


import logging
from django.db.models import TextField
import json


log = logging.getLogger(__name__)


class DataListField(TextField):

    def from_db_value(self, value, expression, connection):
        if not value:
            return []
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except Exception as e:
            log.error(e)
            return []

    def to_python(self, value):
        log.debug("DataListField.to_python")
        if not value:
            return []
        if not isinstance(value, str):
            return value
        try:
            return json.loads(value)
        except Exception as e:
            log.error(e)
            return []

    def get_prep_value(self, value):
        log.debug("DataListField.get_prep_value")
        log.debug(value)
        if not value:
            return json.dumps([])
        if isinstance(value, str):
            return value
        return json.dumps(value, indent=4)

    def value_to_string(self, obj):
        if isinstance(obj, str):
            return obj
        else:
            return json.dumps(obj, indent=4)
