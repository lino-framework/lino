Coming
======

New features
------------

- WYSIWYG editor for `notes.Note.body`.
  

Upgrade instructions
--------------------

The following are technical instructions related to this 
upgrade, designed to be executed by a Lino expert.
For more general instructions on how to upgrade an existing 
Lino site, see :doc:`/admin/upgrade`.

- Edit your local `settings.py` and replace 
  ``APPY_PARAMS`` with ``LINO.appy_params``
  (:doc:`/blog/2011/0531`).
  For example, if you had::

    APPY_PARAMS.update(pythonWithUnoPath='/etc/openoffice.org3/program/python')
  
  then replace this with::
  
    LINO.appy_params.update(pythonWithUnoPath='/etc/openoffice.org3/program/python')
    
- In case you have local fixtures: rename all `.dpy` files to `.py`.
  Change your `dump` script.
  See :doc:`/blog/2011/0601`.


- Database migration: 

  - rename `.dpy` to `.py`
  
  - Adapt your document templates for text fields in Note and Contract.

  - Lino 1.1.11 generated  (empty) generators for the models 
    from :mod:`django.contrib.auth` and :mod:`django.contrib.sessions`.
    And :mod:`django.contrib.sites` now also has been removed.
    Uncomment these lines::
    
        #~ Permission = resolve_model("auth.Permission")
        #~ Group = resolve_model("auth.Group")
        #~ User = resolve_model("auth.User")
        #~ Message = resolve_model("auth.Message")
        #~ Site = resolve_model("sites.Site")
        ...
        #~ Session = resolve_model("sessions.Session")
        
  - (not necessary because TinyMCE also accepts plain text)
    Existing content in `notes.Note.body` must be converted using 
    :func:`lino.utils.restify.restify`.
    See :doc:`/blog/2011/0525`.
    

  