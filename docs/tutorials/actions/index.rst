==============
Actions
==============

.. include:: /include/wip.rst

Actions are one of the concepts which Lino adds to Django.

The whole system is not yet fully stable, 
but this tutorial is a tested document, so you can rely on it ;-)

An Action in Lino is something "which a user can do". 
It is usually represented as a clickable button.

Each Actor has a *default action*. For `dd.Table` this is 
 "GridEdit", which means "open a window showing a grid on this 
table as main widget".
That's why you can define a menu item by simply naming an actor.

Other standard actions on `dd.Table` are things like "Save", "Delete", "Insert".

Where to define actions
-----------------------

You can define actions

- either on the Model or on the Table
- either using the `dd.action` decorator on a method
  or by defining a custom subclass of `dd.RowAction`
  (and adding an instance of this class to the Model or the Table)
  


How to "remove" an inherited action or collected from a table
-------------------------------------------------------------

Given a model `M` defining an action `m`, 
and a table `T` on `M` defining another action `t`, 
when I define a second table `S1(T)`, then `S1` will have 
both actions `m` and `t`::

.. literalinclude:: models.py

..
  >>> # encoding: utf-8
  >>> from lino.runtime import *
  >>> globals().update(actions)


>>> [ba.action for ba in T.get_actions()]
[<SubmitDetail put (u'Save')>, <SubmitInsert post (u'Create')>, <DeleteSelected None (u'Delete')>, <GridEdit grid>, <A a (u'a')>, <RowAction m (u'm')>, <RowAction t (u't')>]

>>> [ba.action for ba in S1.get_actions()]
[<SubmitDetail put (u'Save')>, <SubmitInsert post (u'Create')>, <DeleteSelected None (u'Delete')>, <GridEdit grid>, <A a (u'a')>, <RowAction m (u'm')>, <RowAction t (u't')>]

>>> [ba.action for ba in S2.get_actions()]
[<SubmitDetail put (u'Save')>, <SubmitInsert post (u'Create')>, <DeleteSelected None (u'Delete')>, <GridEdit grid>, <A a (u'a')>]


>>> ses = settings.SITE.login()
>>> obj = M()
>>> ses.run(obj.a)
{'message': u'Called a() on M object', 'success': True}

>>> ses.run(obj.t)
Traceback (most recent call last):
...
AttributeError: 'M' object has no attribute 't'

>>> ses.run(S1.t,obj)
{'message': u'Called t() on M object', 'success': True}
