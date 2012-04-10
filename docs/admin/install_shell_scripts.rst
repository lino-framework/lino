Install shell scripts 
---------------------

You might want to copy some of the Lino utility scripts 
from :srcref:`/bash`
to your project directory and make them executable.

Something like this::

  cd /usr/local/django/myproject
  cp /var/snapshots/lino/bash/* .
  chmod u+x pull oood manage.py dump start stop watch_tim
  
Explanations:

  ===================================== =========================================
  :srcref:`start </bash/start>`         Manually start all local Lino services
  :srcref:`stop </bash/stop>`           Manually stop all local Lino services
  :srcref:`dump </bash/dump>`           Write a dpy dump of your database
  :srcref:`pull </bash/pull>`           Update your copy of Lino sources 
  :srcref:`oood </bash/oood>`           Start or stop OpenOffice (LibreOffice) in server mode
  :srcref:`watch_tim </bash/watch_tim>` Start or stop the :term:`watch_tim` daemon
  ===================================== =========================================

Afterwards you'll have to manually adapt them:

- `start` and `stop` : remove the line for :term:`watch_tim` if you don't need it.
- `oood` : check the path of OpenOffice / LibreOffice
