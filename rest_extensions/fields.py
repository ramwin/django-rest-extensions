#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-10-17 09:31:03


import random
import logging
from django.db.models import Field, TextField
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


class DictField(Field):

    description = "enable mysql or sqlite to store json data"

    def to_python(self, value):
        return json.loads(value)

    def from_db_value(self, value, expression, connection):
        return json.loads(value)


class Color:
    """color"""

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    @classmethod
    def default(cls):
        return cls(255, 255, 255)

    @classmethod
    def random(cls):
        return cls(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            )

    def __eq__(self, color):
        if isinstance(color, Color):
            return self.r == color.r and self.g == color.g and self.b == color.b
        return False

    def __str__(self):
        return "r: {}, g: {}, b: {}".format(self.r, self.g, self.b)

    def __repr__(self):
        return "Color: {}".format(self)


class ColorField(Field):

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 52
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        log.debug("ColorField.deconstruct")
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        return name, path, args, kwargs

    def db_type(self, connection):
        log.debug("ColorField.db_type")
        return "char(52)"

    def from_db_value(self, value, expression, connection):
        log.info("ColorField.from_db_value")
        if value is None:
            return Color.default()
        r, g, b = list(map(lambda x: int(x), value.split(",")))
        return Color(r, g, b)

    def to_python(self, value):
        log.info("ColorField.to_python")
        if isinstance(value, Color):
            return value
        if value is None:
            return Color.default()
        r, g, b = list(map(lambda x: int(x), value.split(",")))
        return Color(r, g, b)

    def get_prep_value(self, value):
        log.debug("ColorField.get_prep_value")
        log.debug(value)
        if value is None:
            return ",".join(["255", "255", "255"])
        return ",".join(map(lambda x: str(x), [value.r, value.g, value.b]))
