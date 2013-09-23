.. _mass_hosting:

Mass hosting Lino applications
==============================

The :attr:`site_prefix <lino.site.Site.site_prefix>` Lino setting is 
used when a Lino instance is not running at the root URL of the server.

::

  ServerName sites.miolino.net
  ServerAdmin luc@miolino.net

  WSGIDaemonProcess sites threads=15
  WSGIProcessGroup sites
  WSGIApplicationGroup %{GLOBAL}

  AliasMatch ^/([^/]+)/media/(.+) /usr/local/lino_sites/$1/media/$2
  <DirectoryMatch ^/usr/local/lino_sites/([^/]+)/media>
  Order deny,allow
  Allow from all
  </DirectoryMatch>

  WSGIScriptAliasMatch ^/([^/]+) /usr/local/lino_sites/$1/wsgi.py
    


