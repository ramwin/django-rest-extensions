#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2019-10-15 22:16:47



from django.core.cache import cache

from rest_framework.authentication import TokenAuthentication


class TokenAuthenticationWithCache(TokenAuthentication):

    def authenticate_header(self, key):
        cache_key = f"valid_key_{key}"
        cache_result = cache.get(cache_key, None)
        if cache_result:
            return cache_result
        result = super().authenticate_credentials(key)
        if result[0].is_authenticated:
            cache.set(cache_key, result, timeout=60 * 5)
        return result
