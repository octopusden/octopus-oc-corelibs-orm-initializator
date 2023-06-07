import unittest
import unittest.mock

import os
import json

import oc_orm_initializator.orm_initializator

# to get rid of garbage output
import logging
logging.getLogger().propagate = False
logging.getLogger().disabled = True

class TestOrmInitializator(unittest.TestCase):

    def test_django_initialization__no_port(self):
        django_settings_mock = unittest.mock.NonCallableMock()
        django_settings_mock.configure = unittest.mock.MagicMock()
        django_mock = unittest.mock.NonCallableMock()
        django_mock.setup = unittest.mock.MagicMock()
        with unittest.mock.patch("oc_orm_initializator.orm_initializator.settings", new=django_settings_mock):
            with unittest.mock.patch("oc_orm_initializator.orm_initializator.django", new=django_mock):
                _orm = oc_orm_initializator.orm_initializator.OrmInitializator(
                        url="db-test.example.com/test-db?search_path=test_schema",
                        user="test_user",
                        password="test_password",
                        installed_apps=["test_app", "another_test_app", "yet_another_test_app"])

        django_settings_mock.configure.assert_called_once_with(
                DATABASES={
                    'default':{
                        'ENGINE': 'django.db.backends.postgresql_psycopg2',
                        'NAME': 'test-db',
                        'USER': 'test_user',
                        'PASSWORD': 'test_password',
                        'HOST': 'db-test.example.com',
                        'PORT': 5432,
                        'OPTIONS': {
                            'options': '-c search_path=test_schema'}}},
                USE_TZ=True,
                TIME_ZONE='Etc/UTC',
                INSTALLED_APPS=list(set([
                    "test_app",
                    "another_test_app",
                    "yet_another_test_app",
                    'django.contrib.contenttypes',
                    'django.contrib.auth'])))

        django_mock.setup.assert_called_once()

    def test_django_initialization__ok(self):
        django_settings_mock = unittest.mock.NonCallableMock()
        django_settings_mock.configure = unittest.mock.MagicMock()
        django_mock = unittest.mock.NonCallableMock()
        django_mock.setup = unittest.mock.MagicMock()
        with unittest.mock.patch("oc_orm_initializator.orm_initializator.settings", new=django_settings_mock):
            with unittest.mock.patch("oc_orm_initializator.orm_initializator.django", new=django_mock):
                _orm = oc_orm_initializator.orm_initializator.OrmInitializator(
                        url="db-test.example.com:5311/another-test-db?search_path=another_test_schema",
                        user="test_user",
                        password="test_password",
                        installed_apps=["test_app", "another_test_app", "yet_another_test_app"])

        django_settings_mock.configure.assert_called_once_with(
                DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.postgresql_psycopg2',
                        'NAME': 'another-test-db',
                        'USER': 'test_user',
                        'PASSWORD': 'test_password',
                        'HOST': 'db-test.example.com',
                        'PORT': 5311,
                        'OPTIONS': {
                            'options': '-c search_path=another_test_schema'}}},
                USE_TZ=True,
                TIME_ZONE='Etc/UTC',
                INSTALLED_APPS=list(set([
                    'test_app', 
                    'another_test_app',
                    'yet_another_test_app',
                    'django.contrib.contenttypes',
                    'django.contrib.auth'])))

        django_mock.setup.assert_called_once()

    def test_django_initialization__no_db_name(self,):
        django_settings_mock = unittest.mock.NonCallableMock()
        django_settings_mock.configure = unittest.mock.MagicMock()
        django_mock = unittest.mock.NonCallableMock()
        django_mock.setup = unittest.mock.MagicMock()
        with unittest.mock.patch("oc_orm_initializator.orm_initializator.settings", new=django_settings_mock):
            with unittest.mock.patch("oc_orm_initializator.orm_initializator.django", new=django_mock):
                with self.assertRaises(ValueError):
                    _orm = oc_orm_initializator.orm_initializator.OrmInitializator(
                            url="db-test.example.com",
                            user="test_user",
                            password="test_password",
                            installed_apps=["test_app", "another_test_app", "yet_another_test_app"])

        django_settings_mock.configure.assert_not_called()
        django_mock.setup.assert_not_called()

    def test_django_initialization__no_opitons(self):
        django_settings_mock = unittest.mock.NonCallableMock()
        django_settings_mock.configure = unittest.mock.MagicMock()
        django_mock = unittest.mock.NonCallableMock()
        django_mock.setup = unittest.mock.MagicMock()
        with unittest.mock.patch("oc_orm_initializator.orm_initializator.settings", new=django_settings_mock):
            with unittest.mock.patch("oc_orm_initializator.orm_initializator.django", new=django_mock):
                with self.assertRaises(ValueError):
                    _orm = oc_orm_initializator.orm_initializator.OrmInitializator(
                            url="db-test.example.com/yet-another-test-db",
                            user="test_user",
                            password="test_password",
                            installed_apps=["test_app", "another_test_app", "yet_another_test_app"])

        django_settings_mock.configure.assert_not_called()
        django_mock.setup.assert_not_called()
