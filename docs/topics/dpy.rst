===================
The .dpy serializer
===================

:xfile:`.dpy` is a data format to be used for serializing 
or deserializing Django database.

There are two big use cases: 
(1) "intelligent" fixtures and 
(2) :doc:`/admin/datamig`

To use it, you simply add the following line
in your :xfile:`settings.py`::

    SERIALIZATION_MODULES = {
        "dpy" : "lino.utils.dpy",
    }
    
(You must of course :doc:`Install Lino </admin/install>` 
in order to have the :mod:`lino.utils.dpy` module installed on your system.)

We choose the file extension `.dpy` because
simply naming them .py would conflict with 
the existing PythonSerializer.

See also

  http://code.djangoproject.com/ticket/10664
 

.dpy fixtures
-------------

When loading a `.dpy` fixture, the corresponding .dpy file 
will be imported like a normal Python module. 

This module can do what you want, but it must define a function `objects` 
which should return or yield the list of model instances 
to be added. Fictive minimal Example::

  from myapp.models import Foo
  def objects():
      yield Foo(name="First")
      yield Foo(name="Second")

  
Here are some examples of real-world fixtures:

- :srcref:`/lino/apps/dsbe/fixtures/demo.dpy`
- :srcref:`/lino/modlib/countries/fixtures/be.dpy`
- :srcref:`/lino/modlib/contacts/fixtures/demo.dpy`
- :srcref:`/lino/modlib/contacts/fixtures/std.dpy`

Note that most of these examples 
use :class:`lino.utils.instantiator.Instantiator`, 
which is just a convenience and not required by the .dpy 
format.




