User and permission management in Lino
======================================

Lino manages users and permissions differently than Django.

User levels

Lino comes with a default list of UserLevels that should suit most needs.


Applications can add customized UserLevels to this list.

What each UserLevel concretely means, depends on the application, 
but there are some general rules of thumb:

- A `guest` can usually see everything, but not edit any data.

- A `user` can usually see everything and edit the data she is responsible for. 
  But not edit any data of other users.

- A `manager` has more rights than a simple `user`. 
  Managers can edit the work of other users.
  
- An `administrator` has even more rights than a `manager`, 
  he can also edit the rights of other users.
  
  
Some entries to the API docs:  
  
- :meth:`lino.dd.Model.get_row_permission`

- :meth:`lino.core.actions.Action.get_action_permission`  

- :meth:`lino.core.actions.Action.get_view_permission`: 
  default is to return `True`, but e.g. 
  :class:`lino.modlib.outbox.CreateMailAction` 
  is not available for users whose email field is blank.


