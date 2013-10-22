.. _mass_hosting:

Mass hosting Lino applications
==============================

Here is a system of files and conventions which we suggest to use
when hosting multiple Lino sites on a same host.

.. include:: /include/wip.rst

.. _lino.djangosite_local:

The `djangosite_local` module
-----------------------------

Create a 
:ref:`djangosite_local.py <djangosite_local>`
file 
with the following content 
in a directory :file:`/usr/local/src/lino`:

.. literalinclude:: djangosite_local.py

Same SECRET_KEY for every project
---------------------------------

Note the line in the above file::

    self.django_settings.update(SECRET_KEY='?~hdakl123ASD%#¤/&¤')
    
It will set the same `SECRET_KEY` for all projects on that server.

If you prefer to use environment variables::

    import os
    ...
    self.django_settings.update(SECRET_KEY=os.environ.get('DJANGO_SECRET_KEY'))


The project directory
---------------------

For every Lino project you then create a "project directory"
with at least the following content:

- a file :xfile:`settings.py` (individual per project),
  often also a Python package, i.e. a directory with at least a 
  file :file:`__init__.py`.

- a file :xfile:`manage.py` (same content for every project):

  .. literalinclude:: manage.py

- a directory :xfile:`apache`
  with a single file :xfile:`wsgi.py` (same content for every project):

  .. literalinclude:: wsgi.py

- a directory :xfile:`media`
- a directory :xfile:`config`


One vhost, many Linos
---------------------

The :setting:`site_prefix` Lino setting is 
used when a Lino instance is not running at the root URL of the server.

The tricky part is to get mod_wsgi to correctly differentiate different 
daemon processes.


`Integration With Django
<https://modwsgi.readthedocs.org/en/latest/integration-guides/django.html>`_

`WSGIDaemonProcess
<https://modwsgi.readthedocs.org/en/latest/configuration-directives/WSGIDaemonProcess.html>`_

`WSGIProcessGroup
<https://modwsgi.readthedocs.org/en/latest/configuration-directives/WSGIProcessGroup.html>`_

`WSGIApplicationGroup
<https://modwsgi.readthedocs.org/en/latest/configuration-directives/WSGIApplicationGroup.html>`_

No WSGI daemon process called '%{RESOURCE}' has been configured

WSGIProcessGroup %{ENV:DJANGO_SETTINGS_MODULE}


No WSGI daemon process called '%{ENV:DJANGO_SETTINGS_MODULE}' has been configured:


::

  ServerName sites.example.com
  ServerAdmin luc@example.com

  WSGIDaemonProcess sites threads=15
  WSGIProcessGroup sites
  WSGIApplicationGroup %{GLOBAL}

  AliasMatch ^/([^/]+)/media/(.+) /usr/local/lino_sites/$1/media/$2
  <DirectoryMatch ^/usr/local/lino_sites/([^/]+)/media>
  Order deny,allow
  Allow from all
  </DirectoryMatch>

  WSGIScriptAliasMatch ^/([^/]+) /usr/local/lino_sites/$1/wsgi.py
    


In your :xfile:`djangosite_local.py` you can write::

    def setup_site(self):
        ...
        if self.site_prefix != '/':
            assert self.site_prefix.endswith('/')
            self.update_settings(SESSION_COOKIE_PATH = self.site_prefix[:-1])
