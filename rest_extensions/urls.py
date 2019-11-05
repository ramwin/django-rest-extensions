#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-11-05 18:06:29


import logging
from rest_framework import routers
from django.apps import apps
from django.urls import path, include
from . import views

log = logging.getLogger(__name__)


log.info("load rest_extensions urls")
log.info(apps.app_configs)
app_name = "rest_extensions"
urlpatterns = [
]


class AppUrls(object):
    """the url for all app"""

    def __init__(self, app_config):
        self.urlpatterns = []
        for model in app_config.get_models():
            self.urlpatterns.append(
                path("{}/multidelete/".format(model.__name__), views.MultiDeleteSerializer),
            )


class AppModelUrl(object):
    pass


for app_key_name in apps.app_configs:
    log.info(app_key_name)
    app_config = apps.app_configs[app_key_name]
    app_urls = AppUrls(app_config)
    log.info("引入app: {}".format(app_key_name))
    urlpatterns.append(
        path("{}/".format(app_key_name), include(app_urls)),
    )
    

app_name = "rest_extensions"


router = routers.DefaultRouter()
log.info(urlpatterns)
