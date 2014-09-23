=======
Actions
=======

.. currentmodule:: dd

.. |disk| image:: ../../lino/media/extjs/images/mjames/disk.png

Overview
--------

Each :class:`Actor` has a list of :class:`Actions <Action>`.

Many actions are installed automatically
(e.g. :class:`DeleteSelected`, ...). Other actions are "custom
actions" defined by the application code.  Lino has a unique API for
writing custom actions in your application.

See also some tutorials:

- :doc:`/tutorials/actions/index`




The ``Action`` class reference
------------------------------

.. class:: Action

  Abstract base class for all Actions.

  .. attribute:: label

  The text to appear on the button.

  .. attribute:: js_handler

  This is usually `None`. Otherwise it is the name of a Javascript
  callable to be called without arguments. That callable must have
  been defined in a :attr:`ad.Plugin.site_js_snippets` of the plugin.

  .. attribute:: help_text

    A help text that shortly explains what this action does.
    ExtJS uses this as tooltip text.

  .. attribute:: parameters

    User-definable parameter fields for this table.
    Set this to a `dict` of `name = models.XyzField()` pairs.

  .. attribute:: params_layout

    If this table or action has parameters, specify here how they
    should be laid out in the parameters panel.

  .. attribute:: params_panel_hidden

    If this table has parameters, set this to True if the parameters
    panel should be initially hidden when this table is being
    displayed.


  .. attribute:: select_rows

    True if this action should be called on a single row (ignoring
    multiple row selection).  Set this to False if this action is a
    list action, not a row action.


  .. attribute:: custom_handler

    Whether this action is implemented as Javascript function call.
    This is necessary if you want your action to be callable using an
    "action link" (html button).

  .. attribute:: show_in_workflow

    Used internally.  Whether this action should be displayed as the
    :meth:`workflow_buttons <dd.Model.workflow_buttons>`
    column. If this is True, then Lino will automatically set
    :attr:`custom_handler` to True.


  .. attribute:: show_in_bbar

     Whether this action should be displayed as a button in the toolbar
     and the context menu.

     For example :class:`ml.beid.FindByBeIdAction` has
     :attr:`show_in_bbar` explicitly set to `False`, otherwise it
     would be visible in the toolbar.

  .. attribute:: auto_save = True

    What to do when this action is being called while the user is on a
    dirty record.
    
    - `False` means: forget any changes in current record and run the
      action.

    - `True` means: save any changes in current record before running
      the action.  `None` means: ask the user.

  .. attribute:: readonly

    Whether this action possibly modifies data *in the given object*.
    
    This means that :class:`InsertRow` is a `readonly` action.
    Actions like :class:`InsertRow` and :class:`Duplicable
    <lino.mixins.duplicable.Duplicate>` which do not modify the given
    object but *do* modify the database, must override their
    `get_action_permission`::
    
      def get_action_permission(self,ar,obj,state):
          if user.profile.readonly:
              return False
          return super(Duplicate,self).get_action_permission(ar,obj,state)

  .. attribute:: icon_name

  The class name of an icon to be used for this action when rendered
  as toolbar button.

  .. attribute:: combo_group = None

  The name of another action to which to "attach" this action.
  Both actions will then be rendered as a single combobutton.

  .. attribute:: sort_index

  Determins the sort order in which the actions will be presented to
  the user.
    
  List actions are negative and come first.
    
  Predefined `sort_index` values are:
    
  ===== =================================
  value action
  ===== =================================
  -1    :class:`as_pdf <lino.utils.appy_pod.PrintTableAction>`
  10    :class:`InsertRow`, :class:`SubmitDetail`
  11    :attr:`duplicate <lino.mixins.duplicable.Duplicable.duplicate>`
  20    :class:`detail <ShowDetailAction>`
  30    :class:`delete <DeleteSelected>`
  31    :class:`merge <MergeAction>`
  50    :class:`Print <lino.mixins.printable.BasePrintAction>`
  51    :class:`Clear Cache <lino.mixins.printable.ClearCacheAction>`
  60    :class:`ShowSlaveTable`
  90    default for all custom row actions
  ===== =================================

  .. method:: run_from_ui(self, ar, **kw)

    Execute the action.  `ar` is an :class:`ActionRequest
    <ar.ActionRequest>` object representing the
    context where the action is running.


  .. method:: FOO_choices

    For every parameter field named "FOO", if the action has a method
    called "FOO_choices" (which must be decorated by
    :func:`dd.chooser`), then this method will be installed as a
    chooser for this parameter field.

  .. method:: get_view_permission(self, profile)

    Return True if this action is visible for users of given profile.

  .. method:: get_action_permission(self, ar, obj, state)

    Return (True or False) whether the given :class:`ar
    <rt.ActionRequest>` should get permission to execute on the given
    Model instance `obj` (which is in the given `state`).

    Derived Action classes may override this to add vetos.
    E.g. the MoveUp action of a Sequenced is not available on the
    first row of given `ar`.


  .. method:: action_param_defaults(self, ar, obj, **kw)

    Same as :meth:`dd.Actor.param_defaults`, except that here it is a
    instance method.

    Note that this method is not called for actions which are rendered
    in a toolbar (:doc:`/tickets/105`)

  .. attribute:: debug_permissions

    Whether to log :ref:`debug_permissions` for this action.
    
  .. attribute:: extjs_main_panel

    Used by `extensible` and `awesome_uploader`.

    Example::

        class CalendarAction(dd.Action):
            extjs_main_panel = "Lino.CalendarApp().get_main_panel()"
            ...


Predefined actions
------------------



.. class:: DeleteSelected

    Delete the row(s) on which it is being executed.

.. class:: EditTemplate

    Edit the print template, i.e. the file specified by
    :meth:`dd.Printable.get_print_templates`.

    The action becomes automatically visible for users with
    `UserLevel` "manager" and when :mod:`lino.modlib.davlink` is
    installed.

    If it is visible, then it still works only when your
    :xfile:`webdav` directory (1) is published by your server under
    "/webdav" and (2) has a symbolic link named `config` which points
    to your local config directory. And (3) the local config directory
    must be writable by `www-data`.
   
.. class:: GridEdit

    Open a window with a grid editor on this table as main item.

.. class:: ShowDetailAction

    Open the Detail Window on an individual row.

.. class:: InsertRow

    Open the Insert window filled with a blank row.  The new row will
    be actually created only when this window gets submitted.


.. class:: SaveRow

    Called when user edited a cell of a non-phantom record in a grid.
    Installed as `update_action` on every :class:`Actor`.

.. class:: MergeAction

    Merge this object into another object of same class.

.. class:: SubmitDetail

    The "Save" button of a :term:`detail window`.
    Rendered as a button with a disk (|disk|).


Writing your own actions
------------------------


.. decorator:: action(*args, **kw)

    Decorator to define custom actions.
    Same signature as :meth:`Action`.
    In practice you'll possibly use:
    :attr:`label <Action.label>`,
    :attr:`help_text <Action.help_text>` and
    :attr:`required <Action.required>`.
    
    The decorated function will be installed as the actions's
    `run_from_ui` method.


  
