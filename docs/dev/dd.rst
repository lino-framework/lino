===============
Data definition
===============

The :mod:`lino.dd` module is a shortcut to those parts of Lino which
are used in your :xfile:`models.py` modules.  The name ``dd`` stands
for "Data Definition".

To keep your application as future-proof as possible, you should use
these shortcuts instead of importing them from their real place.

.. toctree::
   :maxdepth: 2

   actors
   actions


The `dd.Model` class
--------------------

.. class:: dd.Model

  Lino adds a series of features to Django's Model base class.  If a
  Lino application includes plain Django Model classes, Lino will
  "extend" these by adding the attributes and methods defined here to
  these classes.

  .. attribute:: allow_cascaded_delete = []

    A list of names of ForeignKey fields of this model that allow for
    cascaded delete.
    
    When deleting an object through the user interface, Lino by
    default forbids to delete an object that is referenced by other
    objects. Users will get a message of type "Cannot delete X because
    n Ys refer to it".
    
    Example: Lino should not refuse to delete a Mail just because it
    has some Recipient.  When deleting a Mail, Lino should also delete
    its Recipients.  That's why
    :class:`lino.modlib.outbox.models.Recipient` has
    ``allow_cascaded_delete = ['mail']``.
    
    Note that this currently is also consulted by
    :meth:`lino.mixins.duplicable.Duplicable.duplicate` to decide
    whether slaves of a record being duplicated should be duplicated
    as well.
    
    This mechanism doesn't depend on nor influence Django's `on_delete
    <https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.on_delete>`_
    option.  But of course you should not allow_cascaded_delete for
    fields which have e.g. `on_delete=PROTECT`.


Miscellaneous functions
-----------------------

.. function:: dd.fields_list(model, field_names)

Return a set with the names of the specified fields, checking whether
each of them exists.

**Arguments:** `model` is any subclass of `django.db.models.Model`. It
may be a string with the full name of a model
(e.g. ``"myapp.MyModel"``).  `field_names` is a single string with a
space-separated list of field names.

If one of the names refers to a :class:`DummyField`, this name
will be ignored silently.

For example if you have a model `MyModel` with two fields `foo` and
`bar`, then ``dd.fields_list(MyModel,"foo bar")`` will return
``['foo','bar']`` and ``dd.fields_list(MyModel,"foo baz")`` will raise
an exception.

.. class:: dd.DummyField(*args, **kwargs)

Represents a field that doesn't exist in the current configuration but
might exist in other configurations.

.. class:: dd.ForeignKey(othermodel, *args, **kwargs)

This is almost as Django's `ForeignKey
<https://docs.djangoproject.com/en/dev/ref/models/fields/#foreignkey>`
field, except for a subtle difference: it supports `othermodel` being
`None` or the name of some non-installed model and returns a
:class:`DummyField` in that case.  This difference is useful when
designing reusable models.

.. class:: dd.CustomField

Mixin to create a custom field. It defines a single method
:meth:`dd.CustomField.create_layout_elem`


  .. method:: create_layout_elem(self, layout_handle, field, **kw)

     Instantiate and return some subclass of
     :class:`lino.ui.elems.LayoutElement` to be used in
     `layout_handle`.

     `self` and `field` are identical unless self is a RemoteField or
     a :class:`dd.VirtualField`.


.. class:: dd.VirtualField

Represents a virtual field. Virtual fields are not stored in the
database, but computed each time they are read. Django doesn't see
them.

