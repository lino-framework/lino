.. _permissions:

===========
Permissions
===========

.. include:: /include/wip.rst

The :attr:`required <lino.core.actions.Permittable.required>` 
attribute of a table specifies 
which users get permission to view that table.


Two other attributes
:attr:`update_required <lino.core.actors.Actor.update_required>` 
and
:attr:`delete_required <lino.core.actors.Actor.delete_required>` 
can additionally restrict modification permissions
for those users who can *view* a given table.

Default permissions are as follows
::

    class Actor(actions.Parametrizable):
        required = get_default_required()
        update_required = dict()
        delete_required = dict()

All `required` members are dictionaries containing parameters passed 
to :func:`lino.utils.perms.make_permission_handler` (see method description 
for detailed description)

There is a helper function for populating the required user rights.
:func:`lino.utils.auth.get_default_required` (or shortcut 
:func:`lino.dd.required`) method returns "registered users only" 
if :setting:`user_model` is set (authentication is allowed) and no requirements otherwise.
To further restricts permission, pass additional requirements as parameters.

Example: Requires authenticated user with at least "Manager" user level.
::

    required = get_default_required(user_level="manager")


User Object
-----------

Main permissions object is :attr:`user_model <lino.Lino.user_model>`, 
specified in Site configuration. 
See :doc:`/topics/auth`.

If :attr:`user_model <lino.Lino.user_model>` is 'users.User' or 
some sub-class, there is :attr:`profile lino.modlib.users.User`
member that contains user privileges in form of 
:class:`UserProfiles <lino.core.perms.UserProfiles>`.

*TODO: Implement password changing from GUI*

Currently the easiest way to create user and set the password is from 
django shell using following script
::

    from django.conf import settings
    u = settings.SITE.user_model.objects.get(username="TestUserName")
    u.set_password("TestPassword")
    u.save()



.. _user_profile:

User Profile
------------

:class:`lino.utils.auth.UserProfile` defines user privileges. Profiles are defined in Site configuration.

Default profiles are following
::

    add = dd.UserProfiles.add_item
    from lino.core.perms import UserLevels
    add('000', _("Anonymous"),      name='anonymous',   level=None,     authenticated=False)
    add('100', _("User"),           name='user',        level=UserLevels.user)
    add('900', _("Administrator"),  name='admin',       level=UserLevels.admin)

and can be changed in settings.py file:
::

    class Site(Site)
        ...
        def setup_choicelists(self):
            """
            Defines application-specific default user profiles.
            """
            from lino import dd
            from django.utils.translation import ugettext_lazy as _
            from lino.core.perms import UserLevels
            dd.UserProfiles.reset("office system")  # names of UserGroups we want to set specific user level for
            add = dd.UserProfiles.add_item
            add('100', _("Newbie"),     name='anonymous',    level=UserLevels.user,  memberships="G_M") # Gives Newbie a "Guest" Level for "office" User Group and "Manager" Level for "system" group
            add('999', _("Master"),     name='master',       level=UserLevels.expert)
         ...

Each Profile contains information about authorization level. There is possibility to set global User Level for each profile.
User Level is used when determining whether user is authorised to do some action.

Keyword parameter `name` is human-readable name for given profile. First parameter to add_item function is three letter id that is stored in database and uniquely identify the profile.

It is also possible to set different User Level to every User Group by specifying `memberships` keyword to :meth:`lino.utils.auth.UserProfiles.add_item` method.
The value of `membership` parameter can be for example ``"M_M_A"`` and the meaning is, that such profile has User Level of Manager for first two groups and Admin for third group.


User Groups
-----------
Actors can form logical groups defined by modules that usually groups together Actors with similar functionality. User Profile can set specific User Level for each User Group as described in :ref:`user_profile`.
User Groups are defined in modules by calling
::

    dd.add_user_group('uniqueName', _("Human readable name"))


Teams
-----

Team actually does not play any role in permissions. 
They represents some logical grouping of users to user groups and these 
groups can be used throughout the application for different purposes.

For example the :mod:`lino.modlib.cal` uses Teams to 
implement "Send invitation to all teammates".

Authorities
-----------

It is possible to give another user ability to act as myself. 
Option to switch authority is accessible from User menu (rightmost menu item)

This can be handy in situations where one user has to do some work 
on behalf of another user. The typical solution to such situation 
is to share the account credentials. Authorities solves this quite 
common use-case more elegantly.




.. _UserLevels:

User levels
-----------



Lino speaks about user *level* where Plone speaks about user *role*.
Unlike user roles in Plone, user levels are hierarchic:
a "Manager" is higher than a simple "User" and thus 
can do everything for which a simple "User" level has permission.

Each User Level has numerical value assigned. 
Level number is being compared with minimal required level 
when determining privileges.
For example when user level ``50`` if required for specific action, 
only users having user level higher or equal to 50 are authorised.

``UserLevels.SHORT_NAMES`` assigns a one letter long unique id 
that is used when specifying different User Levels for each User Group.



The default UserLevels
----------------------

:class:`UserLevels <lino.core.perms.UserLevels>` has a default list of
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




