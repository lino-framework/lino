Permissions
===========
 

The directories with log files need to be writeable by the Apache process 
("www-data" on a standard Debian).
For example something like this::

  # chgrp -R www-data /var/log/lino
  # chmod -R g+ws /var/log/lino 

``chmod g+s`` sets the SGID to ensure that when a new file is created in the directory 
it will inherit the group of the directory.

You'll probably need to add `umask 002` to your `/etc/apache2/envvars`. 
For example if Lino's `.log` file doesn't exist, 
`www-data` (the user under which Apache is running) will create a new file, 
and that file should be writable by other users of the `www-data` group.

Or the other way: if you launched manually e.g. a
:mod:`initdb <lino.management.commands.initdb>` which created the file, 
user `www-data` must also have write access to this file. 

If you use sqlite, you'll have to do something like this::

  chgrp www-data /usr/local/django/myproject/myproject.db
  chmod -R g+w /usr/local/django/myproject/myproject.db
  
You'll maybe have to do something like this::

  # addgroup YOURSELF www-data
  
In certain cases it may be useful to tidy up::

  $ find ~/hgwork -name '*.pyc' -delete
  
To see which directories are on your Python path::

  python -c "import sys; print sys.path"


Did you know? To watch all log files at once, you can do::

  sudo tail -f /var/log/lino/system.log /var/log/lino/db.log /var/log/apache2/error.log /var/log/apache2/access.log
  
See also the `multitail` package  
  

Set up Mercurial
----------------

Add in your `/etc/mercurial/hgrc`::

  [trusted]
  groups = www-data


