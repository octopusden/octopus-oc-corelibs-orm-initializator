import re
import urllib.parse as urlparse
import django
from django.conf import settings
import posixpath
from copy import deepcopy

class OrmInitializator():
    """
    A base class for DB connection via Django ORM
    """
    def __init__(self, url, user, password, installed_apps=list(), **additional_settings):
        """
        additional settings shoud include: url, user, password, installed_apps
        :param str url: URL for database connection
        :param str user: username for database authentication
        :param str password: password for database authentication
        :param list installed_apps: list of installed django applications
        :param additional_settings: Additional settings for DB connection
        """
        _all_settings = deepcopy(additional_settings)
        _all_settings["DATABASES"] = self._fill_db_dictionary(url=url, user=user, password=password)

        # avoid applications duplication
        _all_settings["INSTALLED_APPS"] = list(set(installed_apps + 
            ['django.contrib.contenttypes', 'django.contrib.auth']))

        # we have to always use time zone in case we do not want to mix timestamps
        _all_settings["USE_TZ"] = True
        _all_settings["TIME_ZONE"] = additional_settings.get("TIME_ZONE") or "Etc/UTC"

        settings.configure(**_all_settings)

        django.setup()
    
    def _fill_db_dictionary(self, url, user, password):
        """
        Returns django settings dictionary with PostgreSQL settings
        :param str url: URL for database connection
        :param str user: username for database authentication
        :param str password: password for database authentication
        :return dict: Django-compatible dictionary of applications
        """
        host, port, dbname, options = self._parse_psql_url(url)

        if not options:
            raise ValueError("Options are required for django configuration")

        return {
            "default": {
                "ENGINE": "django.db.backends.postgresql_psycopg2",
                "NAME": dbname,
                "USER": user,
                "PASSWORD": password,
                "HOST": host,
                "PORT": port,
                "OPTIONS": {"options": "-c " + options},
            }}
    
    def _parse_psql_url(self, url):
        """
        Parses PostgreSQL connection string.
        
        :param url: connection string, which must determine host, port, database name and may determine options
        :returns: hosts, port, database name, options
        """
        if not re.match("(.*?:)?" + posixpath.sep + posixpath.sep, url):
            url = posixpath.sep + posixpath.sep + url

        parse_result = urlparse.urlparse(url)
        host = parse_result.hostname
        port = parse_result.port
        
        # use default PSQL port if not specified:
        if not port:
            port=5432

        dbname = parse_result.path.strip(posixpath.sep)
        options = parse_result.query

        if not all([host, port, dbname]):
            raise ValueError("Invalid PSQL_URL: '%s'. Host, port and dbname are required" % url)

        return host, port, dbname, options
        
