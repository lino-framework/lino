======
Actors
======

Overview
--------

An :class:`Actor <lino.core.actors.Actor>` 
is a globally known unique thing that offers actions.
Each actor has a list of **actions**.
Almost every incoming web request
is a given *user* who requests execution 
of a given *action* on a given *actor*.

Each subclass of an actor is a new actor.

An alternative name for "Actor" might be "Resource" or "View"
(but they are already being used very often).



Actors are classes, not instances
---------------------------------

Actors are never instantiated, we use only the class objects.

The main reason for this design choice is that it leads to more 
readable application code. Consider the following excerpt from 
:mod:`lino.modlib.cal.models`.

.. code-block:: python

    class Guests(dd.Table):
        model = Guest
        required = dd.required(user_groups='office')
        column_names = 'partner role workflow_buttons remark event *'
            
    class GuestsByEvent(Guests):
        master_key = 'event'

    class GuestsByPartner(Guests):
        master_key = 'partner'
        column_names = 'event role workflow_buttons remark *'

    class MyPresences(GuestsByPartner):
        required = dd.required(user_groups='office')
        order_by = ['event__start_date','event__start_time']
        label = _("My presences")
        
        @classmethod
        def get_request_queryset(self,ar):
            ar.master_instance = ar.get_user().partner
            return super(MyPresences,self).get_request_queryset(ar)
    

