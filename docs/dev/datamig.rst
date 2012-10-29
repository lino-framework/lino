Designing data migrations for your application
----------------------------------------------

Designing data migrations for your application
is easy but not yet well documented.

The main trick is the last line of any Python fixture::

    settings.LINO.install_migrations(globals())


This means that the fixture itself will call 
the :meth:`lino.Lino.install_migrations` method of 
your new application *before* actually starting.
And it passes her `globals()` dict, which means 
that you can potentially change everything.


Look at lino_welfare.modlib.pcsw.old_migrate

A magical `before_dumpy_save` attribute may contain custom 
code to apply inside the try...except block. 
If that code fails, the deserializer will simply 
defer the save operation and try it again.
    
