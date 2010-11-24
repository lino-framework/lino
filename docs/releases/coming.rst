Coming
======

New features
------------

- Detail windows now have a Refresh button. 

- New module "Uploads". (See :doc:`/blog/2010/1122`)

- New buttons "Clear cache" and "Edit template" on printables. (See :doc:`/blog/2010/1124`)

- Grid no longer has a bottom toolbar. row actions accessible only through context menu. 
  "Save GC" button now as a window tool button. (See :doc:`/blog/2010/1124`)

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
    
- Move the doctemplates directory (which until now was in 
  ``settings.PROJET_DIR + "/doctemplates"``) 
  to 
  ``settings.MEDIA_ROOT + "/webdav/doctemplates"``. 
  (See :doc:`/blog/2010/1124`)

    
  
- The usual things in your local directory::

    cd /usr/local/django/myproject
    python manage.py initdb_tim
    python manage.py make_staff
  
- Restart Apache::

    sudo /etc/init.d/apache2 restart

