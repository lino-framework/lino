Tables
======

.. contents:: 
   :local:
   :depth: 2



The ``AbstractTable`` class
---------------------------

.. autoclass:: lino.core.tables.AbstractTable
  :members:

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

  .. attribute:: start_at_bottom

    Set this to `True` if you want your table to *start at the bottom*.
    Unlike reverse ordering, the rows remain in their natural order,
    but when we open a grid on this table, we want it to start on the
    last page.
    
    First use case are :class:`ml.sales.InvoicesByJournal`
    and
    :class:`ml.ledger.InvoicesByJournal`.

    New since :doc:`/tickets/143`.


  .. attribute:: slave_grid_format

    How to display this table when it is a slave in a detail
    window. Must be one of the following values:

    - `'grid'` (default) to render as a grid. 
    - `'summary'` to render a summary in a HtmlBoxPanel.
    - `'html'` to render plain html a HtmlBoxPanel.

    Example: :class:`ml.households.SiblingsByPerson`.

  .. attribute:: preview_limit

    The maximum number of rows to fetch when this table is being
    displayed in "preview mode", i.e. (1) as a slave table in a detail
    window or (2) as an item of the :xfile:`admin_main.html` returned
    by :meth:`ad.Site.get_admin_main_items`.

    The default value for this is the :attr:`preview_limit
    <ad.Site.preview_limit>` class attribute of your
    :class:`Site <ad.Site>`, which itself has a hard-coded
    default value of 15 and which you can override in your
    :xfile:`settings.py`.
    
    If you set this to `None`, preview requests for this table will
    request all rows.  Since preview tables usually have no paging
    toolbar, that's theoretically what we want (but can lead to waste
    of performance if there are many rows).
    
    Test case and description in :ref:`cosi.tested`.
    
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



The ``Table`` class
-------------------


.. autoclass:: lino.core.dbtables.Table
  :members:
  :inherited-members:

  .. attribute:: master

    Automatically set to the model pointed to by the
    :attr:`master_key`.  Used also in lino.models.ModelsBySite

  .. attribute:: master_key

    The name of the ForeignKey field of this Table's :attr:`model that
    points to it's :attr:`master`.  Setting this will turn the table
    into a :term:`slave table`.

    The :attr:`master_key` is automatically added to
    :attr:`hidden_columns`.

  .. attribute:: master_field

    For internal use. Automatically set to the field descriptor of the
    :attr:`master_key`.

  .. attribute:: details_of_master_template

    Used to build the title of a request on this table when it is a
    slave of a given master. The default value is defined as follows::

        details_of_master_template = _("%(details)s of %(master)s")

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


  .. attribute:: editable

    Set this explicitly to True or False to make the Actor per se
    editable or not.  Otherwise it will be set to `False` if the Actor
    is a Table and has a `get_data_rows` method.
    
    Non-editable actors won't even call `get_view_permission` for
    actions which are not readonly.
    
    The :class:`lino.modlib.changes.models.Changes` table is an
    example where this is being used: nobody should ever edit
    something in the table of Changes.  The user interface uses this
    to generate optimized JS code for this case.


  .. attribute:: stay_in_grid

    Set this to True if Lino should not open a newly created record in
    a detail window.


The ``VirtualTable`` class
--------------------------


.. autoclass:: lino.core.tables.VirtualTable
    :members:



The ``EmptyTable`` class
--------------------------

.. class:: EmptyTable

    A "Table" that has exactly one virtual row and thus is visible
    only using a Detail view on that row.


The ``VentilatingTable`` class
------------------------------

.. class:: VentilatingTable(AbstractTable)

    A mixin for tables that have a series of automatically generated
    columns

    .. attribute:: ventilated_column_suffix

    .. attribute:: description

    .. method:: setup_columns(self)
    .. method:: get_ventilated_columns(self)



The ``Report`` class
------------------------------

.. class:: Report


    A special kind of :class:`EmptyTable` used to quickly create
    complex "reports". A report is a series of tables combined into a
    single printable and previewable document.


    .. classmethod:: get_story(cls, obj, ar)

    .. attribute:: body(cls, self, ar)


