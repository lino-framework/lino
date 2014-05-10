=======
Layouts
=======

.. currentmodule:: dd


Overview
--------

A layout is an abstract pythonical description of how to visually
arrange the fields, columns and other data elements of a form or a
table.

This section applies to the following attributes of your actors:

- :attr:`column_names <dd.AbstractTable.column_names>`
- :attr:`detail_layout <dd.Actor.detail_layout>` 
- :attr:`insert_layout <dd.Actor.insert_layout>`
- :attr:`params_layout <dd.Actor.params_layout>`
- and for the :attr:`params_layout <dd.Action.params_layout>` of a
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
of :class:`ListLayout`, :class:`FormLayout`.  :class:`ParamsLayout` or
:class:`ActionParamsLayout`.

Lino automatically creates 

- :class:`dd.Panel` and :class:`dd.FormLayout`

See also:

- Tutorial: :doc:`/tutorials/layouts`
- :ref:`lino.tutorial.polls`.
 
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

This is for :class:`ListLayout` and :class:`FormLayout`.

:class:`ParamsLayout` are special but similar: their data elements
refer to the *parameters*  of an actor 
defined in :attr:`dd.Actor.parameters`.


Panels
------

**A Layout consists of "panels".** 

Every layout has at least one panel whose name is ``main``.

When a :attr:`detail_layout <dd.Actor.detail_layout>` is a string,
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

    A Layout description for a Detail Window or an Insert Window.

    Lino instantiates this for every 
    :attr:`detail_layout <dd.Actor.detail_layout>` 
    and for every 
    :attr:`insert_layout <dd.Actor.insert_layout>`.


.. class:: ListLayout

    A layout for describing the columns of a table.

    Lino automatically creates one instance of this for every table
    using the string specified in that table's :attr:`column_names
    <dd.AbstractTable.column_names>` attribute.
    

.. class:: ParamsLayout

    A Layout description for a table parameter panel.

    Lino instantiates this for every actor with 
    :attr:`parameters <dd.Actor.parameters>`,
    based on that actor's
    :attr:`params_layout <dd.Actor.params_layout>`.

.. class:: ActionParamsLayout

   A Layout description for an action parameter panel.

   Lino instantiates this for every :attr:`params_layout
   <dd.Action.params_layout>` of a custom action.

   A subclass of :class:`ParamsLayout`. 

 


