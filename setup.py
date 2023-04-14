#!/usr/bin/env python3

from setuptools import setup

__version="0.0.1"

_spec = {
    "name" : "oc_orm_initializator",
    "packages" : ["oc_orm_initializator"],
    "version" : __version,
    "install_requires": [
        "django==3.2.13", 
        "django-simple-history==3.0.0", 
        "psycopg2"
    ],
    "python_requires": ">=3.6",
    "description" : "Django ORM intialization",
    "long_description": "",
    "long_description_content_type": "text/plain"
}

setup(**_spec)
