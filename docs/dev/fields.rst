===============
Database fields
===============

.. currentmodule:: dd

This section documents custom fields for use in your models.

.. contents:: 
   :local:
   :depth: 2


VirtualField
============

.. class:: VirtualField

Represents a virtual field. Virtual fields are not stored in the
database, but computed each time they are read. Django doesn't see
them.

.. function:: virtualfield(return_type)

Decorator to turn a method into a :class:`VirtualField`.

RequestField
============

.. class:: RequestField

A :class:`VirtualField` whose values are requests.


DummyField
==========

.. class:: DummyField(*args, **kwargs)

Represents a field that doesn't exist in the current configuration but
might exist in other configurations.

ForeignKey
==========

.. class:: ForeignKey(othermodel, *args, **kwargs)

This is almost as Django's `ForeignKey
<https://docs.djangoproject.com/en/dev/ref/models/fields/#foreignkey>`
field, except for a subtle difference: it supports `othermodel` being
`None` or the name of some non-installed model and returns a
:class:`DummyField` in that case.  This difference is useful when
designing reusable models.


CustomField
===========

.. class:: CustomField

Mixin to create a custom field. It defines a single method
:meth:`dd.CustomField.create_layout_elem`


  .. method:: create_layout_elem(self, layout_handle, field, **kw)

     Instantiate and return some subclass of
     :class:`lino.ui.elems.LayoutElement` to be used in
     `layout_handle`.

     `self` and `field` are identical unless self is a RemoteField or
     a :class:`dd.VirtualField`.

