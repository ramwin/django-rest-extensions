#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2017-10-12 11:25:13

from rest_framework import pagination


class PaginationClass(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
