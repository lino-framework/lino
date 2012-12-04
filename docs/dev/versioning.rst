Versioning and release process
==============================

Your application's version is in :attr:`lino.Lino.version`.



Requiring a minimal Lino version
--------------------------------

If you use anything from :mod:`lino.mixins` or :mod:`lino.modlib`,
then your database structure may depend on the Lino version.
So it is possible that your application requires a given Lino 
version.

So do we need an attribute `depends_on_lino_version`?
Not sure. Maybe this should be managed through the 
`Python distutils
<http://wiki.python.org/moin/CheeseShopTutorial>`_.
To be continued.



Intermediate versions
---------------------

An intermediate version is a version whose number ends with a "+".

The "+" causes Lino to raise 
an exception if somebody tried to read or write a dumpy fixture.
This is to keep you from accidentally using this version 
on a production server.

To be more precise, Lino raises 
`Cannot dumpdata from intermediate version X+` in 
:meth:`lino.utils.dumpy.Serializer.serialize`
and 
`Cannot loaddata python dumps to intermediate version X+` 
:meth:`lino.Lino.install_migrations` 





