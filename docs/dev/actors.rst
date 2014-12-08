======
Actors
======

.. currentmodule:: dd

.. contents:: 
   :local:
   :depth: 2


Overview
========

An **actor** is a globally known unique object that offers **actions**.
Almost every incoming web request in a Lino application requests
execution of a given *action* on a given *actor*.

An alternative name for "Actor" might be "Resource" or "View", but
these words are already being used very often, so in Lino we talk
about *actors*.

The most common type of actors are **tables**. A table is an actor
which displays some data in a tabular way, i.e. interactively as a
GridPanel or on a printable document as a table.

Besides *model-based tables* (who display data coming from the
database), Lino has *virtual tables*.

:class:`lino.core.tables.AbstractTable` is the base class for 
:class:`lino.core.tables.Table`  and
:class:`lino.core.tables.VirtualTable` 

The **columns** of a table are defined by attributes like 
:attr:`column_names <lino.core.tables.AbstractTable.column_names>`.

The **rows** of a table are defined by a method :meth:`get_data_rows
<lino.core.tables.AbstractTable.get_data_rows>` which, in a
model-based table has a default implementation based on the
:attr:`model <lino.core.tables.Table.model>` attribute.

Not all actors are tables. Another type of actors are *frames* which
display some data in some other form. One such frame actor is the
calendar panel, another one is :class:`EmptyTable`, used to display
reports.

See also

- :doc:`/tutorials/vtables/index`
- :doc:`/tutorials/tables/index`
- :doc:`/tutorials/actors/index`

The application namespace
=========================

When we say that actors are "globally known unique objects", then we
refer to what we call the **application namespace**.

Actually the application namespace is split across two places:
:data:`dd.plugins`
:data:`rt.modules`



Actors are classes, not instances
=================================

Actors are never instantiated, we use only the class objects.  Lino
will automatically register each subclass of :class:`Actor` as an
actor.

The main reason for this design choice is that it leads to more
readable application code.  But it has some disadvantages:

- Every method of an actor must have a `@classmethod` decorator.

- Concepts like `Parametrizable` are common to actions and actors, but
  need a "class method" and an "instance method" version of their
  logic.

We might decide one day that Lino creates an automatic singleton
instance for each Actor at startup.



The ``Actor`` class
===================


.. autoclass:: lino.core.actors.Actor
    :members:


The following class methods are `None` in the default
implementation. Subclass can defines them.


.. py:classmethod:: Actor.get_handle_name(self, ar)

    Most actors use the same UI handle for each request.  But
    e.g. :class:`welfare.debts.PrintEntriesByBudget` overrides this to
    implement dynamic columns depending on it's master_instance.


.. py:classmethod:: Actor.get_row_classes(self, ar)

    If a method of this name is defined on an actor, then it must be a
    class method which takes an :class:`rt.ar` as single
    argument and returns either None or a string "red", "green" or
    "blue" (todo: add more colors and styles). Example::

        @classmethod
        def get_row_classes(cls,obj,ar):
            if obj.client_state == pcsw.ClientStates.newcomer:
                return 'green'

    Defining this method will cause an additional special
    `RowClassStoreField` field in the :class:`lino.ui.Store` objects
    of this actor.

.. py:classmethod:: Actor.get_welcome_messages(self, ar)

    If a method of this name is defined on an actor, then it must be a
    class method which takes an :class:`rt.ar` as single
    argument and returns or yields a list of :term:`welcome messages
    <welcome message>` (messages to be displayed in the welcome block
    of :xfile:`admin_main.html`).



.. class:: Actor2

  See :class:`lino.core.actors.Actor`.

  .. attribute:: required
  .. attribute:: update_required
  .. attribute:: delete_required
  .. attribute:: parameters
  .. attribute:: params_layout
  .. attribute:: detail_layout
  .. attribute:: insert_layout
  .. attribute:: title
  .. attribute:: hide_top_toolbar
  .. attribute:: debug_permissions
  .. attribute:: label
  .. attribute:: insert_layout_width
  .. attribute:: workflow_state_field
  .. attribute:: workflow_owner_field
  .. attribute:: hide_sums
  .. attribute:: hide_window_title
  .. attribute:: window_size
  .. attribute:: app_label
  .. attribute:: abstract
  .. attribute:: allow_create
  .. attribute:: sort_index
  .. attribute:: icon_name
  .. method:: get_pk_field(self)
  .. method:: get_row_by_pk(self, ar, pk)
  .. method:: get_create_permission(self, ar)

  .. method:: apply_cell_format(self, ar, row, col, recno, td)

  .. method:: parse_req(cls, ar, rqdata, **kw)

    This is called when an incoming web request on this actor is being
    parsed.

    If you override :meth:`parse_req`, then keep in mind that it will
    be called *before* Lino checks the requirements.  For example the
    user may be AnonymousUser even if the requirements won't let it be
    executed.  `ar.subst_user.profile` may be None, e.g. when called
    from `find_appointment` in :class:`welfare.pcsw.Clients`.



  .. method:: show(self, master_instance=None, column_names=None,
                   **known_values):

    Creates an action request for this actor and calls its
    :meth:`show <lino.core.actions.ActionRequest.show>`
    method.
    This is a shortcut for usage in tested document snippets.

  .. method:: override_column_headers(self, ar)

    Dynamically override the column headers. This has no effect on a
    GridPanel, only in printed documents or plain html.

  .. method:: get_data_elem(self, name)
    
    Find data element in this actor by name.

  .. method:: get_title(self, ar)

    Return the title of this actor for the given request `ar`.

    Override this if your Table's title should mention for example
    filter conditions.  See also :meth:`dd.Table.get_title`.

  .. method:: get_detail_title(self, ar, obj)

    Return the string to use when building the title of a
    detail window on a given row of this actor.

  .. method:: get_actor_label(self)

    Compute the label of this actor.

  .. method:: get_view_permission(self, profile)

    Return True if this actor as a whole is visible for users with
    the given profile.


  .. method:: get_row_permission(cls, obj, ar, state, ba)

    Returns True or False whether the given action
    is allowed for the given row instance `row`
    and the user who issued the given ActionRequest `ar`.

  .. method:: get_choices_text(self, obj, request, field)

    Return the text to be displayed in a combo box
    for the field `field` of this actor to represent
    the choice `obj`.
    Override this if you want a customized representation.
    For example :class:`lino_faggio.models.InvoiceItems`

  .. method:: setup_request(self, ar)

    Customized versions may e.g. set `master_instance`
    before calling super() (outbox.MyOutbox or mixins.ByUser).

    Other usages are more hackerish:
    - :class:`lino.modlib.households.models.SiblingsByPerson`
    - :class:`lino_welfare.modlib.cal.models.EventsByClient`

    :class:`lino_welfare.pcsw.models.Home`,
    :class:`lino.modlib.users.models.Mysettings`.



  .. attribute:: label

    The text to appear e.g. on a button that will call the default
    action of an actor.  This attribute is *not* inherited to
    subclasses.  For :class:`dd.Table` subclasses that don't have a
    label, Lino will call :meth:`get_actor_label`.

  .. attribute:: abstract

    Set this to `True` to prevent Lino from generating useless
    JavaScript if this is just an abstract base class to be inherited
    by other actors.

  .. method:: workflow_buttons(self, obj, ar)

  .. method:: get_data_elem(self, name)
    
  .. method:: get_title(self, ar)

  .. method:: get_detail_title(self, ar, obj)

    Return the string to use when building the title of a
    detail window on a given row of this actor.

  .. method:: get_actor_label(self)

    Compute the label of this actor.

  .. method:: get_view_permission(self, profile)

    Return True if this actor as a whole is visible for users with
    the given profile.


  .. method:: get_row_permission(cls, obj, ar, state, ba)

    Returns True or False whether the given action
    is allowed for the given row instance `row`
    and the user who issued the given ActionRequest `ar`.

  .. method:: get_choices_text(self, obj, request, field)

    Return the text to be displayed in a combo box
    for the field `field` of this actor to represent
    the choice `obj`.
    Override this if you want a customized representation.
    For example :class:`lino_faggio.models.InvoiceItems`

  .. method:: setup_request(self, ar)

    Customized versions may e.g. set `master_instance`
    before calling super() (outbox.MyOutbox or mixins.ByUser).

    Other usages are more hackerish:
    - :class:`lino.modlib.households.models.SiblingsByPerson`
    - :class:`lino_welfare.modlib.cal.models.EventsByClient`

  .. method:: disabled_fields(cls, obj, ar)

    Return a set of field names that should not be editable
    for the specified `obj` and `request`.

    If defined in the Actor, this must be a class method that accepts
    two arguments `obj` and `ar` (an `ActionRequest`)::

      @classmethod
      def disabled_fields(cls, obj, ar):
          ...
          return set()

    If not defined in the Table, Lino will look whether the Table's
    model has a `disabled_fields` method and install a wrapper to this
    model method.  When defined on the model, is must be an *instance*
    method::

      def disabled_fields(self,ar):
          ...
          return set()

    See also :doc:`/tickets/2`.


  .. method:: disabled_actions(self, ar, obj)

    Returns a dictionary containg the names of the actions
    that are disabled  for the given object instance `obj`
    and the user who issued the given ActionRequest `ar`.

    Application developers should not need to override this method.

    Default implementation returns an empty dictionary.
    Overridden by :class:`dd.Table`


  .. method:: request(self, *args, **kw) 

    Return a programmatically instantiated :class:`rt.ar`
    on this actor.

  .. method:: param_defaults(self, ar, **kw)

    Return a dict with default values for the :attr:`parameters`.
    This will be called per request.

    Usage example. The Clients table has a parameter `coached_since`
    whose default value is empty::

      class Clients(dd.Table):
          parameters = dd.ParameterPanel(
            ...
            coached_since=models.DateField(blank=True))

    But `NewClients` is a subclass of `Clients` with the only
    difference that the default value is `amonthago`::


      class NewClients(Clients):
          @classmethod
          def param_defaults(self,ar,**kw):
              kw = super(NewClients,self).param_defaults(ar,**kw)
              kw.update(coached_since=amonthago())
              return kw




The ``Frame`` class
===================

.. class:: Frame

  Base clase for actors which open a window but, but this window is
  neither a database table nor a detail form.

  Example subclass is :class:`ml.extensible.CalendarPanel`.
