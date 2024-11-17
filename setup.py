#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Xiang Wang @ 2019-02-18 15:41:36

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-rest-extensions",
    version="1.2.0",
    author="Xiang Wang",
    author_email="ramwin@qq.com",
    description="create normal api for all your models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ramwin/django-rest-extensions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "django>=2",
        "djangorestframework",
    ],
)
