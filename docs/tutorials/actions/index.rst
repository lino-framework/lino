==============
Custom actions
==============

.. include:: /include/wip.rst

For an introduction, see :ref:`dev.actions`.

The action API is not yet fully stable, but this tutorial is a tested
document, so you can rely on it ;-)

Here is the :xfile:`models.py` file we will use for this tutorial:

.. literalinclude:: models.py

We define a model `Moo` with two actions `a` and `m`, 
and a table `Moos` on `Moo` defining another two action `b` and `t`.


..
  >>> # encoding: utf-8
  >>> from lino.api.shell import *
  >>> globals().update(actions.__dict__)
  >>> from pprint import pprint


Where to define actions
-----------------------

You can define actions

- either on the Model or on the Table


- either using the `dd.action` decorator on a method
  or by defining a custom subclass of `lino.core.actions.Action <lino.core.actions.Action>`
  (and adding an instance of this class to the Model or the Table)
  
  
To demonstrate this, we log in and instantiate an `Moo` object:

>>> ses = rt.login()
>>> obj = Moo()

Running an action programmatically is done using the 
:meth:`run <lino.core.requests.BaseRequest.run>` method of your 
session.

Since `a` and `m` are defined on the Model, we can run them directly:

>>> ses.run(obj.a)
{'message': 'Called a() on Moo object', 'success': True}

>>> ses.run(obj.m)
{'message': 'Called m() on Moo object', 'success': True}

This wouldn't work for `t` and `b` since these are defined on `Moos` 
(which is only one of many possible tables on model `Moo`):

>>> ses.run(obj.t)
Traceback (most recent call last):
...
AttributeError: 'Moo' object has no attribute 't'

So in this case we need to specify them table as the first parameter.
And because they are row actions, we need to pass the instance as 
mandatory first argument:

>>> ses.run(S1.t, obj)
{'message': 'Called t() on Moo object', 'success': True}

>>> ses.run(S1.b, obj)
{'message': 'Called a() on Moo object', 'success': True}

  
How to "remove" an inherited action or collected from a table
-------------------------------------------------------------

Here are the actions on Moos:

>>> pprint([ba.action for ba in Moos.get_actions()])
[<ShowAsHtml show_as_html (u'HTML')>,
 <SaveRow grid_put>,
 <CreateRow grid_post (u'grid_post')>,
 <SubmitInsert submit_insert (u'Create')>,
 <DeleteSelected delete_selected (u'Delete')>,
 <GridEdit grid>,
 <A a (u'a')>,
 <A b (u'a')>,
 <Action m (u'm')>,
 <Action t (u't')>]

A subclass inherits all actions from her parent.
When I define a second table `S1(Moos)`, then `S1` will have 
both actions `m` and `t`:

>>> pprint([ba.action for ba in S1.get_actions()])
[<ShowAsHtml show_as_html (u'HTML')>,
 <SaveRow grid_put>,
 <CreateRow grid_post (u'grid_post')>,
 <SubmitInsert submit_insert (u'Create')>,
 <DeleteSelected delete_selected (u'Delete')>,
 <GridEdit grid>,
 <A a (u'a')>,
 <Action m (u'm')>,
 <A b (u'a')>,
 <Action t (u't')>]

S2 does not have these actions because we "removed" them by overriding
them with None:

>>> pprint([ba.action for ba in S2.get_actions()])
[<ShowAsHtml show_as_html (u'HTML')>,
 <SaveRow grid_put>,
 <CreateRow grid_post (u'grid_post')>,
 <SubmitInsert submit_insert (u'Create')>,
 <DeleteSelected delete_selected (u'Delete')>,
 <GridEdit grid>]



