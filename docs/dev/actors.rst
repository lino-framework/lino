======
Actors
======

.. currentmodule:: dd


Overview
========

An :class:`Actor <dd.Actor>` is a globally known unique thing that
offers :class:`actions <dd.Action>`.

Almost every incoming web request in a Lino application is a given
*user* who requests execution of a given *action* on a given *actor*.

An alternative name for "Actor" might be "Resource" or "View", but
these words are already being used very often, so in this section we
talk about *actors*.

When we say "a globally known unique thing", then we refer to the
global namespace which is currently in :data:`dd.modules`.


**Actors are classes, not instances** : Actors are never instantiated,
we use only the class objects.  Each subclass of an actor is
automatically registered as a new actor.

The main reason for this design choice was that it leads to more
readable application code. This is not an absolute decision,
however. We might decide one day that Lino creates an automatic
singleton instance for each Actor at startup. That would avoid us to
write all those `@classmethod` decorators.


The most common type of actors are tables. A table is an actor which
displays some data in a tabular way, i.e. interactively as a GridPanel
or on a printable document as a table.

:class:`AbstractTable` is the base class for 
:class:`Table`  and
:class:`VirtualTable` 

There are VirtualTable and "normal" (model-based) tables. And then
there is a third kind of table is special: the EmptyTable.

The **columns** of a table are defined by attributes like 
:attr:`column_names <AbstractTable.column_names>`.

The **rows** of a table are defined by a method
:meth:`AbstractTable.get_data_rows` which, in a model-based table has
a default implementation based on the :attr:`model <Table.model>`
attribute.

See also

- :doc:`/tutorials/vtables/index`
- :doc:`/tutorials/tables/index`
- :doc:`/tutorials/actors/index`




The ``Actor`` class
===================

.. class:: Actor

  Base class for
  :class:`AbstractTable <lino.core.tables.AbstractTable>`,
  :class:`ChoiceList <lino.core.choicelists.ChoiceList>`
  and :class:`Frame <lino.core.frames.Frame>`.

  .. attribute:: detail_layout

    Define the form layout to use for the detail window.  Actors
    without :attr:`detail_layout` don't have a show_detail action.

  .. attribute:: insert_layout

    Define the form layout to use for the insert window.  If there's a
    :attr:`detail_layout` but no :attr:`insert_layout`, Lino will use
    :attr:`detail_layout` for the insert window.
    
  .. attribute:: title

    The text to appear e.g. as window title when the actor's default
    action has been called.  If this is not set, Lino will use the
    :attr:`label` as title.

  .. attribute:: hide_top_toolbar

    Whether a Detail Window should have navigation buttons, a "New"
    and a "Delete" buttons.  In ExtJS UI also influences the title of
    a Detail Window to specify only the current element without
    prefixing the Tables's title.
    
    This option is True in 
    :class:`lino.models.SiteConfigs`,
    :class:`lino_welfare.pcsw.models.Home`,
    :class:`lino.modlib.users.models.Mysettings`.



  .. attribute:: debug_permissions

    Whether to log :ref:`debug_permissions` for this actor.


  .. attribute:: label

    The text to appear e.g. on a button that will call the default
    action of an actor.  This attribute is *not* inherited to
    subclasses.  For :class:`dd.Table` subclasses that don't have a
    label, Lino will call :meth:`get_actor_label`.

  .. attribute:: insert_layout_width

    When specifying an :attr:`insert_layout` using a simple a multline
    string, then Lino will instantiate a FormPanel with this width.

  .. attribute:: workflow_state_field

    The name of the field that contains the workflow state of an
    object.  Subclasses may override this.

  .. attribute:: workflow_owner_field

    The name of the field that contains the user who is considered to
    own an object when `Rule.owned_only` is checked.

  .. attribute:: hide_sums

  .. attribute:: hide_window_title

    This is set to `True` e.h. in home pages
    (e.g. :class:`lino_welfare.modlib.pcsw.models.Home`).


    Set this to True if you don't want Lino to display sums in a table
    view.

  .. attribute:: window_size

    Set this to a tuple of (height, width) in pixels to have this
    actor display in a modal non-maximized window.

  .. attribute:: app_label

    Specify this if you want to "override" an existing actor.
    
    The default value is deduced from the module where the subclass is
    defined.
    
    Note that this attribute is not inherited from base classes.
    
    :func:`lino.core.table.table_factory` also uses this.


  .. attribute:: abstract

    Set this to `True` to prevent Lino from generating useless
    JavaScript if this is just an abstract base class to be inherited
    by other actors.

  .. attribute:: allow_create

    If this is False, then then Actor won't have no insert_action.

  .. method:: get_create_permission(self, ar)

    Dynamic test per request.
    This is being called only when :attr:`allow_create` is True.

  .. method:: get_row_classes(self, ar)

    If a method of this name is defined on an actor, then it must be a
    class method which takes an :class:`rt.ActionRequest` as single
    argument and returns either None or a string "red", "green" or
    "blue" (todo: add more colors and styles). Example::
    
        @classmethod
        def get_row_classes(cls,obj,ar):
            if obj.client_state == pcsw.ClientStates.newcomer:
                return 'green'
    
    Defining this method will cause an additional special
    `RowClassStoreField` field in the :class:`lino.ui.Store` objects
    of this actor.



  .. method:: get_welcome_messages(self, ar)

    If a method of this name is defined on an actor, then it must be a
    class method which takes an :class:`rt.ActionRequest` as single
    argument and returns or yields a list of messages to be displayed
    in the welcome block of :xfile:`admin_main.html`.

  .. method:: get_handle_name(self, ar)

    Most actors use the same UI handle for each request.  But
    e.g. :class:`welfare.debts.PrintEntriesByBudget` overrides this to
    implement dynamic columns depending on it's master_instance.


  .. method:: workflow_buttons(self, obj, ar)

    A virtual field that displays the workflow buttons for the given
    row `obj` and `ar`.

    `obj` is an instance of this table's row class,
    `ar` is the :class:`rt.ActionRequest`.

  .. method:: parse_req(cls, ar, rqdata, **kw)

    This is called when an incoming web request on this actor is being
    parsed.

    If you override `parse_req`, then keep in mind that it will be
    called *before* Lino checks the requirements.  For example the
    user may be AnonymousUser even if the requirements won't let it be
    executed.  `ar.subst_user.profile` may be None, e.g. when called
    from `find_appointment` in :ref:`welfare.pcsw.Clients`.



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

    A virtual field that displays the workflow buttons for the given
    row `obj` and `ar`.

    `obj` is an instance of this table's row class,
    `ar` is the :class:`rt.ActionRequest`.

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

    Return a programmatically instantiated :class:`rt.ActionRequest`
    on this actor.

  .. method:: param_defaults(self, ar, **kw)

    Return a dict with default values for the parameters of a request.

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




Tables
======


The ``AbstractTable`` class
---------------------------

.. class:: AbstractTable

    An AbstractTable is the definition of a tabular data view,
    usually displayed in a Grid (but it's up to the user
    interface to decide how to implement this).

    Base class for :class:`Table` and :class:`VirtualTable`.

  .. attribute:: variable_row_height

    Set this to `True` if you want each row to get the height that it
    needs.


  .. attribute:: cell_edit

    `True` to use ExtJS CellSelectionModel, `False` to use RowSelectionModel.
    When True, the users cannot select multiple rows.
    When False, the users cannot select and edit individual cells.

  .. attribute:: column_names

    A string that describes the list of columns of this table.

    Default value is ``'*'``.

    Lino will automatically create a :class:`dd.ListLayout` from this.

    This string must not contain any newline characters because a
    ListLayout's `main` panel descriptor must be horizontal.



  .. method:: get_column_names(self, ar)

    Dynamic tables must subclass this method

  .. method:: get_filter_kw(self, ar, **kw)

    Return a dict with the "master keywords" for this table
    and a given `master_instance`.

    :class:`lino.modlib.tickets.models.EntriesBySession`
    Blog Entries are not directly linked to a Session, but in the
    Detail of a Session we want to display a table of related blog
    entries.

    :class:`lino.modlib.households.models.SiblingsByPerson`
    Household members are not directly linked to a Person, but
    usually a Person is member of exactly one household, and in
    the Detail of a Person we want to display the members of that
    household.


  .. method:: request(self, master_instance=None, **kw)

    Return a new :class:`rt.TableRequest` on this table.  

    If this is a slave table, the :attr:`master_instance
    <rt.TableRequest.master_instance>` can be specified as optional
    positional argument.

  .. attribute:: hide_zero_rows

    Set this to `True` if you want to remove rows which contain no 
    values when rendering this table as plain HTML.
    This is ignored when rendered as ExtJS.


  .. attribute:: auto_fit_column_widths

    Set this to `True` if you want to have the column widths adjusted
    to always fill the available width.  This implies that there will
    be no horizontal scrollbar.

  .. attribute:: hidden_columns

    If given, this is specifies the data elements that should be
    hidden by default when rendering this table.  Example::

      hidden_columns = "long_name expected_date"

    **Value** : Application code should specify this as a *single
    string* containing a space-separated list of field names.  Lino
    will automatically resolve this during server startup using
    :func:`dd.fields_list`.  The runtime value of this attribute is a
    *set of strings*, each one the name of a data element. Defaults to
    an empty set.

    **Inheritance** : Note that this can be specified either on a
    :class:`dd.Model` or on a :class:`dd.Table`.  Lino will make a
    union of both.

  .. attribute:: active_fields

    A list of field names that are "active". 
    Value and inheritance as for :attr:`hidden_columns`.

    When a field is "active", this means only that it will cause an
    immediate "background" save and refresh of the :term:`detail
    window` when their value was changed. The true "activity"
    (i.e. other fields being updated according to the value of an
    active field) is defined in the model's :meth:`full_clean
    <dd.Model.full_clean>` and :meth:`FOO_changed
    <dd.Model.FOO_changed>` methods.

    Note that active fields are active only in a :term:`detail
    window`, not in an :term:`insert window`.  That's because there
    they would lead to the unexpected behaviour of closing the window.


  .. attribute:: slave_grid_format = 'grid'

    How to display this table when it is a slave in a detail window. 
    `grid` (default) to render as a grid. 
    `summary` to render a summary in a HtmlBoxPanel.
    `html` to render plain html a HtmlBoxPanel.
    Example: :class:`links.LinksByController`

  .. attribute:: preview_limit

    The maximum number of rows to fetch when this is being used in
    "preview mode", e.g. as a slave table in a detail window.

    Default value is taken from :attr:`lino.Site.preview_limit`.
    
    If you set this to `None`, preview requests for this table will
    request all rows.  Since preview tables usually have no paging
    toolbar, that's theoretically what we want (but can lead to waste
    of performance if there are many rows).
    
    The default value for this is the :attr:`preview_limit
    <lino.site.Site.preview_limit>` class attribute of your
    :class:`Site <lino.site.Site>`, which itself has a hard-coded
    default value of 15 and which you can override in your
    :xfile:`settings.py`.
    
    Test case and description  in :ref:`cosi.tested`.
    
  .. method:: get_data_rows(self, ar)

    Virtual tables *must* define this method, normal (model-based)
    tables *may* define it.

    This will be called with a
    :class:`lino.core.requests.TableRequest` object and is expected to
    return or yield the list of "rows"::
    
        @classmethod
        def get_data_rows(self, ar):
            ...
            yield somerow
            
    Model tables may also define such a method in case they need local
    filtering.

  .. method:: set_detail_layout(self, *args, **kw)

    Update the :attr:`detail_layout` of this actor, or create a new
    layout if there wasn't one before.

    The first argument can be either a string or a :class:`FormLayout
    <dd.FormLayout>` instance.  If it is a string, it will replace the
    currently defined 'main' panel.  With the special case that if the
    current main panel is horizontal (i.e. the layout has tabs) it
    replaces the 'general' tab.

  .. method:: set_insert_layout(self, *args, **kw)

    Update the :attr:`insert_layout` of this actor,
    or create a new layout if there wasn't one before.
    Otherwise same usage as :meth:`set_detail_layout`.

  .. method:: get_slave_summary(self, obj, ar)

    Return the HTML paragraph to be displayed in the
    TableSummaryPanel when :attr:`slave_grid_format` is `summary`.

    Lino internally creates a virtualfield ``slave_summary`` on each
    table which invokes this method.


The ``VirtualTable`` class reference
------------------------------------

.. class:: VirtualTable

    An :class:`AbstractTable` that works on an volatile (non
    persistent) list of rows.

    By nature it cannot have database fields, only virtual fields.

    Subclasses must define a :meth:`get_data_rows` method.


The ``Table`` class reference
-----------------------------

.. class:: Table

A table that works on a Django Model using a QuerySet.

A table inherits from :class:`AbstractTable` and adds attributes like
:attr:`model` and :attr:`master` and :attr:`master_key` who are
important because Lino handles relations automagically.

Another class of attributes are `filter`, `exclude` and `sort_order`
which are thin wrappers to Django's query lookup parameters of same
name.

  .. attribute:: model = None

    The model on which this table iterates.

  .. attribute:: master = None

    Automatically set to the model pointed to by the
    :attr:`master_key`.  Used also in lino.models.ModelsBySite

  .. attribute:: master_key = None

    The name of the ForeignKey field of this Table's :attr:`model that
    points to it's :attr:`master`.  Setting this will turn the table
    into a :term:`slave table`.

    The :attr:`master_key` is automatically added to
    :attr:`hidden_columns`.

  .. attribute:: master_field = None

    For internal use. Automatically set to the field descriptor of the
    :attr:`master_key`.

  .. attribute:: use_as_default_table = True

    Set this to `False` if this Table should *not* become the Model's
    default table.


  .. attribute:: known_values

    A `dict` of `fieldname` -> `value` pairs that specify "known values".

    Requests will automatically be filtered to show only existing
    records with those values.  This is like :attr:`filter`, but new
    instances created in this Table will automatically have these
    values set.

  .. attribute:: filter

    If specified, this must be a `models.Q` object (not a dict of
    (fieldname -> value) pairs) which will be used as a filter.

    Unlike :attr:`known_values`, this can use the full range of
    Django's `field lookup methods
    <https://docs.djangoproject.com/en/dev/topics/db/queries/#field-lookups>`_

    Note that if the user can create rows in a filtered table, you
    should make sure that new records satisfy your filter condition by
    default, otherwise you can get surprising behaviour if the user
    creates a new row.

    If your filter consists of simple static values on some known
    field, then you'll prefer to use :attr:`known_values` instead of
    :attr:`filter.`


  .. attribute:: editable = None

    Set this explicitly to True or False to make the Actor per se
    editable or not.  Otherwise it will be set to `False` if the Actor
    is a Table and has a `get_data_rows` method.
    
    Non-editable actors won't even call `get_view_permission` for
    actions which are not readonly.
    
    The :class:`lino.modlib.changes.models.Changes` table is an
    example where this is being used: nobody should ever edit
    something in the table of Changes.  The user interface uses this
    to generate optimized JS code for this case.


  .. attribute:: stay_in_grid = False

    Set this to True if Lino should not open a newly created record in
    a detail window.


