.. _dev.actions:

=======================
Introduction to actions
=======================

Actions are one of the concepts which Lino adds to Django.

An Action in Lino is something "which a user can do".  It is often
represented as a clickable button.

Each :class:`Actor <lino.core.actors.Actor>` has its own list of actions.

Each Actor has a *default action*. For :class:`dd.Table
<lino.core.dbtables.Table>` this is "GridEdit", which means "open a
window showing a grid on this table".  That's why you can define a
menu item by simply naming an actor.

Other standard actions on a :class:`dd.Table <lino.core.dbtables.Table>`
are things like "Save", "Delete", "Insert".

Predefined actions are installed automatically
(e.g.
:class:`GridEdit <lino.core.actions.GridEdit>`
:class:`ShowDetailAction <lino.core.actions.ShowDetailAction>`
:class:`DeleteSelected <lino.core.actions.DeleteSelected>`
:class:`InsertRow <lino.core.actions.InsertRow>`
, ...).

Other actions are "custom
actions" defined by the application code.  Lino has a unique API for
writing custom actions in your application.

The Lino Polls tutorial shows the simplest form for defining an action
using a decorated method.

In general we recommend to rather define a class.

Examples of custom actions:

- The :class:`MoveUp <lino.mixins.sequenced.MoveUp>` and
  :class:`MoveDown <lino.mixins.sequenced.MoveDown>` actions of a
  :class:`Sequenced <lino.mixins.sequenced.Sequenced>`.

- The :class:`Duplicate <lino.mixins.duplicable.Duplicate>` action for
  creating a copy of the current row.

- In :mod:`lino.mixins.printable`: 
  :class:`DirectPrintAction <lino.mixins.printable.DirectPrintAction>`,
  :class:`CachedPrintAction <lino.mixins.printable.CachedPrintAction>`,
  :class:`ClearCacheAction <lino.mixins.printable.ClearCacheAction>`

- The :class:`ToggleChoice <lino.modlib.polls.ToggleChoice>`
