.. _layouts:

=======================
Introduction to layouts
=======================

.. currentmodule:: lino.core.layouts

A layout is an abstract pythonical description of how to visually
arrange the fields, columns and other data elements of a form or a
table.

Layouts are used for the following attributes of your tables and
actions:

- :attr:`column_names <dd.AbstractTable.column_names>`
- :attr:`detail_layout <lino.core.actors.Actor.detail_layout>` 
- :attr:`insert_layout <lino.core.actors.Actor.insert_layout>`
- :attr:`params_layout <lino.core.actors.Actor.params_layout>`
- and for the :attr:`params_layout <lino.core.actions.Action.params_layout>` of a
  custom action.

For simple layouts it is enough to specify them just as a string
template. For example::

  column_names = "id name:20 comment:40"

  detail_layout = """
  id name
  description
  comment
  """

Lino will automatically convert such string templates into instances
of :class:`ColumnsLayout`, :class:`FormLayout`.  :class:`ParamsLayout` or
:class:`ActionParamsLayout`.

See also:

- Tutorial: :doc:`/tutorials/layouts`
- :ref:`lino.tutorial.polls`.
- Layouts API: :mod:`lino.core.layouts`
 
Some blog entries with more examples of layout definition:

- :blogref:`20120630`


Data elements
-------------

A layout template is a string containing words, where each word is the
name of a *data element*.

**Data elements** can be 

- database fields
- virtual fields
- :term:`slave tables <slave table>`
- panels

This is for :class:`ColumnsLayout` and :class:`FormLayout`.

:class:`ParamsLayout` are special but similar: their data elements
refer to the *parameters* of an actor defined in
:attr:`lino.core.actors.Actor.parameters`.


Panels
------

**A Layout consists of "panels".** 

Every layout has at least one panel whose name is ``main``.

When a :attr:`detail_layout <lino.core.actors.Actor.detail_layout>` is a string,
then Lino replaces this by a :class:`FormLayout` instance whose `main`
panel is that string.



Writing layouts as classes
--------------------------

In more complex situations it may be preferrable or even necessary to
define your own layout class.  

You do this by subclassing :class:`FormLayout`

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

  class Partners(dd.Table):
      ...
      detail_layout = PartnerDetail()




Each panel is a class attribute defined on your subclass, containing a
string value to be used as template describing the content of that
panel.

It can define more panels whose names may be chosen by the application
developer (just don't chose the name :attr:`window_size` which has a
special meaning, and don't start your panel names with an underscore
because these are reserved for internal use).


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

