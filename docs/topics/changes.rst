Keeping Track of Changes
========================

Since logging of database changes will inevitably cause some extra work, 
this feature is optional per site and per model.

Usage instructions for application developers:

- Override the :meth:`lino.Lino.on_site_startup` 
  method of your Lino instance (in your application's :xfile:`settings.py`) 
  with something like this::

    def on_site_startup(self):
        self.modules.contacts.Person.watch_changes()
        super(Lino,self).on_site_startup()
        
  See :meth:`lino.core.model.watch_changes` for possible parameters.
        
- In the :attr:`lino.core.actors.detail_layout` of 
  your `contact.Person` include the ``lino.ChangesByObject`` 
  slave table.
  
  :class:`lino.models.ChangesByObject`
  


Implementation 

- :mod:`lino.core.changes`
- :class:`lino.models.Change`
