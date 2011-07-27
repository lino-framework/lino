How to migrate data
===================

Here is how we suggest to 
:doc:`migrate existing data </topics/datamig>` 
using :doc:`/topics/dpy`.

Go to your local directory::

  cd /use/local/django/myproject

Run the :srcref:`stop </bash/stop>` command (a bash script to shut down all 
application services)::

  ./stop
  
Create a dpy dump by invoking the :srcref:`dump </bash/dump>` script::

  ./dump
  
This will create a file :file:`dYYYMMDD.py` in your 
local `fixtures` directory 

(YYYYMMDD is the current date, the 
script will refuse to overwrite an existing file. 
If you need more than one dump on the same day, 
then we suggest to rename the dYYYYMMDD.py to dYYYYMMDDa.py)
 
Depending on the changes that come with the upgrade,
it may be necessary to edit the dump file. 
See the release notes for instructions.
  
  nano fixtures/dYYYMMDD.py
  
Now you can call :srcref:`pull </bash/pull>` to upgrade 
your local copy of the Lino source repository::

  ./pull
  
Then use Lino's :mod:`initdb <lino.management.commands.initdb>` 
command to reset the database and reload the dump::
  
  python manage.py initdb dYYYMMDD
  
Restart application services using the :srcref:`start </bash/start>` 
command::
  
  ./start

