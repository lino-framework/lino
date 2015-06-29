.. _permissions:

===========
Permissions
===========

Lino adds enterprise-level concepts for definining permissions. This
includes a replacement for Django's User model. 

.. note:: this document needs update after 20150627

User roles
==========




Specifying the required roles


The :attr:`required <lino.core.actors.Actor.required>` attribute of a
table specifies the conditions that must be met in order to get
permission to view that table.

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

Main permissions object is :attr:`lino.core.site.Site.user_model`, 
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
