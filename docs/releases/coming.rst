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

- Database migration: 
  Existing content in `notes.Note.body` must be converted using 
  :func:`lino.utils.restify.restify`.
  See :doc:`/blog/2011/0525`.