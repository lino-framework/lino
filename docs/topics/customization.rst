=============
Customization
=============

Lino comes with :mod:`lino.modlib` a library of reusable models.
Since life is always more complex than any library, 
we need techniques to make application-specific modifications 
to these modules.
We call it "customization".

A Lino application is itself a Django module and must be listed in Django's 
:setting:`INSTALLED_APPS`.

There is an importand difference between 
customization functions and a `site_setup` function: 

- Customization functions are called at the module level, 
  i.e. unconditionally when the application's `models` module
  is imported.
  They are formulated as separate functions just for 
  maintainablilty and documentation.
  
  This means that they are called 
  *before Django populates his model cache*. 
  That's why they can inject fields using :func:`lino.dd.inject_field`.
  
  
- The `site_setup` function in contrast gets called only 
  when Lino starts up.  
  Django has don'e his work and it's too late to make changes 
  the database structure.



