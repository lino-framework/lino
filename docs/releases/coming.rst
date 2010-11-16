Coming
======

New features
------------

- Detail window now has a Refresh button.  

Bugs fixed
----------

- Standard values on a phantom row are no longer visible.  (:doc:`/blog/2010/1116`)

- Coachings and user were missing in a Person's detail.  (:doc:`/blog/2010/1116`)

- performance of previous/next buttons in Detail view of 
  reports with over thousand records might be better. (:doc:`/blog/2010/1116`)

- problem of distorted pictures might be solved (:doc:`/blog/2010/1116`)


Upgrade instructions
--------------------

- Upgrade your copy of the Lino sources::

    cd /var/snapshots/lino
    hg pull -u
  
- The usual things in your local directory::

    cd /usr/local/django/myproject
    python manage.py initdb_tim
    python manage.py make_staff
  
- Restart Apache::

    sudo /etc/init.d/apache2 restart

