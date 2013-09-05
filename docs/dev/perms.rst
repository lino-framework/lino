.. _permissions:

===========
Permissions
===========

.. include:: /include/wip.rst


.. _UserLevels:

User levels
===========

Lino speaks about user *level* where Plone speaks about user *role*.
Unlike user roles in Plone, user levels are hierarchic:
a "Manager" is higher than a simple "User" and thus 
can do everything for which a simple "User" level has permission.



The default UserLevels
----------------------

:class:`UserLevels <lino.core.auth.UserLevels>` has a default list of
user levels which we recommend to use when possible. 
Otherwise you can redefine your own by overriding 
:meth:`lino.site.Site.setup_choicelists` and 
resetting `dd.UserLevels`.

The default list of user levels is as follows:

  .. django2rst:: settings.SITE.login().show(lino.UserLevels)
  

.. _UserLevels.user:

user
~~~~~~~

A normal user.
  

.. _UserLevels.guest:

guest
~~~~~~~

Authenticated but has less rights than a normal user.
  

.. _UserLevels.admin:

admin
~~~~~~~

The highest user level. 


.. _UserLevels.manager:

manager
~~~~~~~

An manager is between a user and an administrator.
About the difference between "Administrator" and "Manager":

- "Management is closer to the employees. 
  Admin is over the management and more over the money 
  of the organization and lilscencing of an organization. 
  Mananagement manages employees. 
  Admin manages the outside contacts and the 
  facitlity as a whole." (`answerbag.com <http://www.answerbag.com/q_view/295182>`__)

- See also a more detailed overview at
  http://www.differencebetween.com/difference-between-manager-and-vs-administrator/






Level-based versus class-based
------------------------------

Maybe we once replace the level-based system by a class-based system of 
user roles.

For example there was once
a **"restricted"** user level used in 
:mod:`lino.modlib.postings`: 
the idea was that "secretaries" do certain general jobs 
for the "specialists".
They are members of the same "user groups", 
but have less rights than the "real users". 
They are more than "guests" however.
Thus the need for an intermediate level.
But this was maybe an unnecessary complication. 
Removed it. Waiting for concrete use-case.




