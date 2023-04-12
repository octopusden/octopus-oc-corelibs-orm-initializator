# Django ORM initializator class

Initialize Django ORM basing on settings (*url, user, password, applications list*)

*URL* have to be in the form:

```
database.host.fqdn:port/database_name?search_path=schema_name
```

*applications list* is a list of strings, each one means Python module of corresponding Django application.


## Limitations

- The only backend supported is PSQL (**psycopg2**)
- Some Django applicatoins are hardcodly appended and should be installed anywhere:
    - django.contrib.contenttypes
    - django.contrib.auth
