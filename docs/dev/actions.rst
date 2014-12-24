.. _dev.actions:

=======================
Introduction to actions
=======================

Actions are one of the concepts which Lino adds to Django.

An Action in Lino is something "which a user can do".  It is usually
represented as a clickable button.


Each :class:`Actor` has a list of :class:`Actions <Action>`.

Predefined actions are installed automatically
(e.g.
:class:`GridEdit`
:class:`ShowDetailAction`
:class:`DeleteSelected`
:class:`InsertRow`
, ...).

Other actions are "custom
actions" defined by the application code.  Lino has a unique API for
writing custom actions in your application.





The Lino Polls tutorial shows the simplest form for defining an action
using the decorator.

In general we recommend to rather define a class.


Each Actor has a *default action*. For `dd.Table` this is 
"GridEdit", which means "open a window showing a grid on this table".
That's why you can define a menu item by simply naming an actor.

Other standard actions on `dd.Table` are things like 
"Save", "Delete", "Insert".





