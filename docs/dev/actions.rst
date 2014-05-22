=======
Actions
=======

.. currentmodule:: dd


Overview
--------

Each :class:`Actor` has a list of :class:`Actions <Action>`.

Many actions are installed automatically
(e.g. :class:`DeleteSelected`, ...). Other actions are "custom
actions" defined by the application code.

Lino has a unique API for writing custom actions in your application.

See also some tutorials:

- :doc:`/tutorials/actions/index`




The ``Action`` class reference
------------------------------

.. class:: Action

  Abstract base class for all Actions.

  .. attribute:: label = None

  The text to appear on the button.

  .. attribute:: help_text = None

    A help text that shortly explains what this action does.
    ExtJS uses this as tooltip text.

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
  -1    :class:`as_pdf <lino.utils.appy_pod.PrinttableAction>`
  10    :class:`insert <InsertRow>`, SubmitDetail
  11    :attr:`duplicate <lino.mixins.duplicable.Duplicable.duplicate>`
  20    :class:`detail <ShowDetailAction>`
  30    :class:`delete <DeleteSelected>`
  31    :class:`merge <lino.mixins.mergeable.Merge>`
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


.. class:: DeleteSelected

    Delete the row(s) on which it is being executed.

.. class:: ShowDetailAction

    Open the Detail Window on an individual row.

.. class:: InsertRow

    Open the Insert window filled with a blank row.  The new row will
    be actually created only when this window gets submitted.


.. class:: SaveRow

    Called when user edited a cell of a non-phantom record in a grid.
    Installed as `update_action` on every :class:`Actor`.

.. decorator:: action(*args, **kw)

    Decorator to define custom actions.
    Same signature as :meth:`Action`.
    In practice you'll possibly use:
    :attr:`label <Action.label>`,
    :attr:`help_text <Action.help_text>` and
    :attr:`required <Action.required>`.
    
    The decorated function will be installed as the actions's
    `run_from_ui` method.
