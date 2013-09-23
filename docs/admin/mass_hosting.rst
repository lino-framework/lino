.. _mass_hosting:

Mass hosting Lino applications
==============================

The :attr:`site_prefix <lino.site.Site.site_prefix>` Lino setting is 
used when a Lino instance is not running at the root URL of the server.

.. include:: /include/wip.rst

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
