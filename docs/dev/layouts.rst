=======
Layouts
=======

.. currentmodule:: dd


Overview
--------

This section documents the classes used when working with Layouts:

- :class:`dd.Panel` and :class:`dd.FormLayout`

- The internally used classes 
  :class:`ListLayout`,
  :class:`ParamsLayout` and :class:`ActionParamsLayout`
  and their common base class :class:`BaseLayout`

- The runtime classes :class:`LayoutHandle`

See also:

- Tutorial: :doc:`/tutorials/layouts`


Form Layouts
------------

A form layout is an abstract pythonical description of how to arrange
the fields and other elements of a form.

For simple form layouts it is enough to specify just a string
template. For example::

  detail_layout = """
  id name
  description
  """

You can do this for the following attributes of your :attr:`Actor
<lino.core.actors.Actor>` subclass::

- :attr:`detail_layout <lino.core.actors.Actor.detail_layout>` 
- :attr:`insert_layout <lino.core.actors.Actor.insert_layout>`
- :attr:`params_layout <lino.core.actors.Actor.params_layout>`

Additionally you can do this for the :attr:`params_layout
<lino.core.actions.Action.params_layout>` of a custom action.

Lino will automatically convert such a string template into an
instance of :class:`FormLayout`.  See :ref:`lino.tutorial.polls`.

In more complex situations it may be preferrable or even necessary to
define your own layout class.  You do this by subclassing
:class:`FormLayout`

.  For example::

  class PartnerDetail(dd.FormLayout):
      main = """
      id name
      description contact
      """
      contact = """
      phone
      email
      url
      """

Lino differentiates between "data layouts" and "parameter layouts".

A layout template (the value of a panel attribute) is a string
containing words, where each word is the name of a *data element*.

**Data elements** can be 

- database fields
- table fields
- another panel
- a :term:`slave tables <slave table>`
- a parameter

This is for :class:`ListLayout` and :class:`FormLayout`.

:class:`ParamsLayout` are special but similar: their data elements
refer to the *parameters*  of an actor 
defined in :attr:`dd.Actor.parameters`.


**A Layout consists of "panels".** Each panel is a class attribute
defined on your subclass, containing a string value to be used as
template describing the content of that panel.  A Layout must define
at least a ``main`` panel.  It can define more panels whose names may
be chosen by the application developer (just don't chose the name
:attr:`window_size` which has a special meaning, and don't start you
panel names with an underscore because these are reserved for internal
use).


Panels are **either horizontal or vertical**, depending on whether
their template contains at least one newline character or not.

Indentation doesn't matter.

If the `main` panel of a :class:`FormLayout` is horizontal, 
ExtJS will render the Layout using as a tabbed main panel. 
If you want a horizontal main panel instead, just insert 
a newline somewhere in your main's template. Example::


  class NoteLayout(dd.FormLayout):
      left = """
      date type subject 
      person company
      body
      """
      
      right = """
      uploads.UploadsByController
      cal.TasksByController
      """
      
      # the following will create a tabbed main panel:
      
      main = "left:60 right:30"
      
      # to avoid a tabbed main panel, specify:
      main = """
      left:60 right:30
      """

List Layouts
------------

A :class:`ListLayout` is a special case for describing the columns of
a GridPanel and therefore may contain only one `main` panel descriptor
which must be horizontal.  ListLayouts are created automatically by
Lino, using the :attr:`column_names
<lino.core.actors.Actor.column_names>` attribute of the Actor as
`main` panel.

A :class:`ParamsLayout` is a special case for describing the layout of
a parameters panel.

Some blog entries with more examples of layout definition:

- :blogref:`20120630`



Classes reference
-----------------

.. class:: BaseLayout

    Base class for all Layouts (:class:`FormLayout`, :class:`ListLayout`
    and  :class:`ParamsLayout`).

    A Layout instance just holds the string templates.
    It is designed to be subclassed by applications programmers.


    In some cases we still use the (reprecated)  methods
    :meth:`set_detail_layout <dd.Actor.set_detail_layout>`,
    :meth:`set_insert_layout <dd.Actor.set_insert_layout>`,
    :meth:`add_detail_panel <dd.Actor.add_detail_panel>`
    and
    :meth:`add_detail_tab <dd.Actor.add_detail_tab>`
    on the :class:`Actor <dd.Actor>`.


.. class:: FormLayout

    A Layout description for the main panel of a DetailWindow or InsertWindow.

.. class:: ListLayout

    A Layout description for the columns of a :class:`Table`.

    Lino will automatically create an instance of this from 
    :attr:`dd.Table.column_names`.

.. class:: ParamsLayout

    A Layout description for a table parameter panel.

.. class:: ActionParamsLayout

   A subclass of :class:`ParamsLayout`. 

   A Layout description for an action parameter panel.



