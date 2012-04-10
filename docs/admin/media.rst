The `media` directory
=====================

The `media` directory is a subdirectory of your project directory, 
containing symbolic links to various sets of static files which Lino
expects to be served under the `/media/` location.

The **development server** will mount it automatically.
On a **production server** you will add a line like the following 
to your Apache config::

  Alias /media/ /usr/local/django/myproject/media/
  
Description of the individual `media` sub-directories:

- /media/lino/ :       Lino's :srcref`/media` directory
- /media/extjs/ :      ExtJS library (:attr:`lino.Lino.extjs_root`)
- /media/extensible/ : Ext.ensible library (:attr:`lino.Lino.extensible_root`)
- /media/tinymce/ :    TinyMCE library (:attr:`lino.Lino.tinymce_root`)

Lino will automatically create the following subdirectories 
if they don't exist:

- /media/cache/ : temporary files created by Lino
- /media/uploads/ : Uploaded files
- /media/webdav/ : User-editable files 

There may be application-specific media subdirectories,
for example:

- /media/beid/  : image files for pcsw.models.PersonDetail    


