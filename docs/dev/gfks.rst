========================
GenericForeignKey fields
========================

The `GenericForeignKey` field (GFK) is a great feature provided by
Django's `django.contrib.contenttypes
<https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/>`_
module. While a normal `ForeignKey` field can point to a database
object *of a given model*, a `GenericForeignKey` can point to a
database object *of any model*.

This section provides a topic overview. See also
:doc:`/tutorials/gfks/index` and
:mod:`test_broken_gfks <lino_welfare.projects.eupen.tests.test_broken_gfks>`).


In order to use GFKs, you must have ``django.contrib.contenttypes`` in
your :setting:`INSTALLED_APPS`. In a Lino application we recommend to
use :mod:`lino.modlib.contenttypes`, which is a thin wrapper around
Django's original app. This gives you additional functionality:

- the :class:`Controllable <lino.modlib.contenttypes.mixins,Controllable>`
  model mixin 
- the :class:`BrokenGFKs :<lino.modlib.contenttypes.models.BrokenGFKs>` table

Lino's :meth:`disable_delete <lino.core.model.Model.disable_delete>`
method tests for related objects, which automatically includes also
those which are related using a GFK. non-nullable and warning before
message.

Another problem is that in Django this automatism happens only if the
object being deleted has a `GenericRelation
<https://docs.djangoproject.com/en/1.7/ref/contrib/contenttypes/#django.contrib.contenttypes.fields.GenericRelation>`_
field. 

In Lino you can configure the cascading behaviour using the
:attr:`allow_stale_generic_foreignkey
<lino.core.model.Model.allow_stale_generic_foreignkey>`.

