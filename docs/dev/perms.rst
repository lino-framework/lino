.. _permissions:

===========
Permissions
===========

Lino adds enterprise-level concepts for definining permissions. This
includes a replacement for Django's User model.

See also: :doc:`users`.


User roles
==========

Certain objects in Lino have a :attr:`roles_required
<lino.core.permissions.Permittable.roles_required>` attribute which
specifies the user roles required for getting permission to access
this resource.  Where "resource" is one of the following:

- an actor :class:`lino.core.actors.Actor` 
- an action :class:`lino.core.actions.Action` 
- a panel :class:`lino.core.layouts.Panel` 

User profiles
=============

User roles are just class objects which represent conditions for
getting permission to access miscellaneous functionalities.  They are
things that *may* act as a requirement.  Every plugin may define its
own user roles which may inherit from other roles defined by other
plugins

At some moment, a site administrator needs to assign a role to every
user. In this situation it would be irritating to see all roles at
this moment.  Not all user roles are meaningful in a given
application.  So we need to define a *subset of all available roles*
for that application.  This is done using the :class:`UserProfiles
<lino.modlib.users.choicelists.UserProfiles>` choicelist.

The :class:`UserProfiles <lino.modlib.users.choicelists.UserProfiles>`
choicelist

- defines the subset of roles to be made available
- it gives a translatable name to every role
- it assigns a value to every choice in order to store that profile


And then the :attr:`profile <lino.modlib.users.models.User.profile>`
field of :class:`users.User <lino.modlib.users.models.User>` model is
used to assign such a profile to a given user.


Local customizations
====================

You may have noted that :class:`UserProfiles
<lino.modlib.users.choicelists.UserProfiles>` is a choicelist, not a
database table.  This is because it depends on the application and is
usually not locally modified.  

Local site administrators may nevertheless decide to change the set of
available user profiles.

A user profile may have additional attributes which influence the user
interface:


- :attr:`hidden_languages
  <lino.modlib.users.choicelists.UserProfile.hidden_languages>` 

- :attr:`readonly <lino.modlib.users.choicelists.UserProfile.readonly>` 


The user profiles module
========================

The :attr:`roles_required
<lino.core.permissions.Permittable.roles_required>` attribute is being
ignored when :attr:`user_profiles_module
<lino.core.site.Site.user_profiles_module>` is empty.


.. xfile:: roles.py

The :xfile:`roles.py` is used for both defining roles and profiles the
user roles that we want to make available in a given application.
Every profile is assigned to one and only one user role. But not every
user role is made available for selection in the




.. _debug_permissions:

Permission debug messages
-------------------------

Sometimes you want to know why a given action is available (or not
available) on an actor where you would not (or would) have expected it
to be.

In this situation you can temporarily set the `debug_permissions`
attributes on both the :attr:`Actor <lino.core.actors.Actor.debug_permissions>` and
the :attr:`Action <lino.core.actions.Action.debug_permissions>` to True.

This will cause Lino to log an info message for each invocation of a
handler on this action.

Since you probably don't want to have this feature accidentally
activated on a production server, Lino will raise an Exception if this
happens when :setting:`DEBUG` is False.
