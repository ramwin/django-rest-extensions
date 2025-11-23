#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-11-05 18:06:29


import logging
from rest_framework import routers
from django.apps import apps
from django.urls import path, include
from . import views

log = logging.getLogger(__name__)


log.debug("load rest_extensions urls")
log.debug(apps.app_configs)
app_name = "rest_extensions"
router = routers.DefaultRouter()
api_urlpatterns = []


class AppUrls(object):
    """the url for all app"""

    def __init__(self, app_config):
        self.urlpatterns = []
        self.app_name = app_config.name
        self.app_module = app_config.module
        for model in app_config.get_models():
            model_view_set = views.ModelViewSetFactory(
                self.app_module, model, app_config).create_view_set()
            router.register(model.__name__, model_view_set)
            self.urlpatterns.append(
                path("{}/multidelete/".format(model.__name__),
                     views.MultiDeleteSerializer),
            )
        self.urlpatterns += router.urls


class AppModelUrl(object):
    pass


for app_key_name in apps.app_configs:
    log.debug(app_key_name)
    app_config = apps.app_configs[app_key_name]
    app_urls = AppUrls(app_config)
    log.debug("load app: {}".format(app_key_name))
    api_urlpatterns.append(
        path("{}/".format(app_key_name), include(
            app_urls, namespace=app_key_name)),
    )
    log.debug(app_urls.urlpatterns)

app_name = "rest_extensions"
urlpatterns = list(api_urlpatterns)
