Installing a `watch_tim` daemon
-------------------------------

This is only for :term:`TIM` users who use Lino in parallel with TIM. 
`watch_tim` keeps an individually configured set of data in sync with 
the TIM data.

Create a directory 
:file:`/usr/local/django/myproject/watch_tim` 
and a :file:`/usr/local/django/myproject/watch_tim/run` 
with something like::
  
  #!/bin/bash
  MYPROJECT="myproject"
  PROJECT_DIR="/usr/local/django/$MYPROJECT"
  PID="$PROJECT_DIR/watch_tim/pid"
  DJANGO_SETTINGS_MODULE=$MYPROJECT.settings
  python $PROJECT_DIR/manage.py watch_tim --pidfile $PID /path/to/TIM/changelog
  
Don't forget to do ``chmod 755 watch_tim/run``.

Then, as root, copy Lino's startup template :srcref:`/bash/watch_tim` 
to your :file:`/etc/init.d` directory and edit the copy::

  # cp /var/snapshots/lino/bash/watch_tim /etc/init.d
  # chmod 755 /etc/init.d/watch_tim
  # nano /etc/init.d/watch_tim

In this file you must edit at least the content of variable `MYPROJECT`.
Check manually whether the script works correctly::

  # /etc/init.d/watch_tim start
  # /etc/init.d/watch_tim stop
  # /etc/init.d/watch_tim restart

And finally::

  # update-rc.d watch_tim defaults
  
In case of problems, see also 
:mod:`lino.modlib.dsbe.management.commands.watch_tim`  





