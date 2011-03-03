Coming
======


Upgrade instructions
--------------------

- Database migration needed because:

    - 

- Go to your local directory::

    cd /usr/local/django/myproject
    
- Stop application services::

    ./stop
    
- Update the source code::

    ./pull
    python manage.py test dsbe
    
  Note: 
  For some apps the tests are currently broken. 
  That's just because we didn't yet find time to maintain them.
  We're working on it.

    
- When a data migration is necessary, see :doc:`/admin/datamig`

