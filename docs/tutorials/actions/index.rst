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
"GridEdit", which means "open a window showing a grid on this table".
That's why you can define a menu item by simply naming an actor.

Other standard actions on `dd.Table` are things like 
"Save", "Delete", "Insert".


Here is the :xfile:`models.py` file we will use for this tutorial:

.. literalinclude:: models.py

We define a model `Moo` with two actions `a` and `m`, 
and a table `Moos` on `Moo` defining another two action `b` and `t`.


..
  >>> # encoding: utf-8
  >>> from lino.runtime import *
  >>> globals().update(actions)
  >>> from pprint import pprint


Where to define actions
-----------------------

You can define actions

- either on the Model or on the Table


- either using the `dd.action` decorator on a method
  or by defining a custom subclass of `dd.RowAction`
  (and adding an instance of this class to the Model or the Table)
  
  
To demonstrate this, we log in and instantiate an `Moo` object:

>>> ses = settings.SITE.login()
>>> obj = Moo()

Running an action programmatically is done using the 
:meth:`run <lino.core.requests.BaseRequest.run>` method of your 
session.

Since `a` and `m` are defined on the Model, we can run them directly:

>>> ses.run(obj.a)
{'message': u'Called a() on Moo object', 'success': True}

>>> ses.run(obj.m)
{'message': u'Called m() on Moo object', 'success': True}

This wouldn't work for `t` and `b` since these are defined on `Moos` 
(which is only one of many possible tables on model `Moo`):

>>> ses.run(obj.t)
Traceback (most recent call last):
...
AttributeError: 'Moo' object has no attribute 't'

So in this case we need to specify them as the first parameter.
And becasue they are row actions, we need to pass the instance as 
mandatory first argument:

>>> ses.run(S1.t,obj)
{'message': u'Called t() on Moo object', 'success': True}

>>> ses.run(S1.b,obj)
{'message': u'Called a() on Moo object', 'success': True}

  
How to "remove" an inherited action or collected from a table
-------------------------------------------------------------

When I define a second table `S1(Moos)`, then `S1` will have 
both actions `m` and `t`:


>>> pprint([ba.action for ba in Moos.get_actions()])
[<SubmitDetail put (u'Save')>,
 <SubmitInsert post (u'Create')>,
 <DeleteSelected None (u'Delete')>,
 <GridEdit grid>,
 <A a (u'a')>,
 <A b (u'a')>,
 <RowAction m (u'm')>,
 <RowAction t (u't')>]

A subclass inherits all actions from her parent:

>>> pprint([ba.action for ba in S1.get_actions()])
[<SubmitDetail put (u'Save')>,
 <SubmitInsert post (u'Create')>,
 <DeleteSelected None (u'Delete')>,
 <GridEdit grid>,
 <A a (u'a')>,
 <RowAction m (u'm')>,
 <A b (u'a')>,
 <RowAction t (u't')>]


>>> pprint([ba.action for ba in S2.get_actions()])
[<SubmitDetail put (u'Save')>,
 <SubmitInsert post (u'Create')>,
 <DeleteSelected None (u'Delete')>,
 <GridEdit grid>]


