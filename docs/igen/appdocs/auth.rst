====
auth
====



.. currentmodule:: auth

Defined in :srcref:`/lino/modlib/auth/models.py`


This is a stripped copy of `django.contrib.auth`.



.. contents:: Table of Contents



.. index::
   pair: model; Permission

.. _igen.auth.Permission:

--------------------
Model **Permission**
--------------------



The permissions system provides a way to assign permissions to specific users and groups of users.

    The permission system is used by the Django admin site, but may also be useful in your own code. The Django admin site uses permissions as follows:

        - The "add" permission limits the user's ability to view the "add" form and add an object.
        - The "change" permission limits a user's ability to view the change list, view the "change" form and change an object.
        - The "delete" permission limits the ability to delete an object.

    Permissions are set globally per type of object, not per specific object instance. It is possible to say "Mary may change news stories," but it's not currently possible to say "Mary may change news stories, but only the ones she created herself" or "Mary may only change news stories that have a certain status or publication date."

    Three basic permissions -- add, change and delete -- are automatically created for each Django model.
    
  
============ ========== ==============================================================
name         type       verbose name                                                  
============ ========== ==============================================================
id           AutoField  ID                                                            
name         CharField  name                                                          
content_type ForeignKey content type (Inhaltstyp,type de contenu,inhoudstype,sisutüüp)
codename     CharField  codename                                                      
============ ========== ==============================================================

    
Defined in :srcref:`/django/contrib/auth/models.py`

.. index::
   single: field;id
   
.. _igen.auth.Permission.id:

Field **Permission.id**
=======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _igen.auth.Permission.name:

Field **Permission.name**
=========================





Type: CharField

   
.. index::
   single: field;content_type
   
.. _igen.auth.Permission.content_type:

Field **Permission.content_type**
=================================





Type: ForeignKey

   
.. index::
   single: field;codename
   
.. _igen.auth.Permission.codename:

Field **Permission.codename**
=============================





Type: CharField

   


.. index::
   pair: model; Group_permissions

.. _igen.auth.Group_permissions:

---------------------------
Model **Group_permissions**
---------------------------



Group_permissions(id, group_id, permission_id)
  
========== ========== ============
name       type       verbose name
========== ========== ============
id         AutoField  ID          
group      ForeignKey group       
permission ForeignKey permission  
========== ========== ============

    
Defined in :srcref:`/django/contrib/auth/models.py`

.. index::
   single: field;id
   
.. _igen.auth.Group_permissions.id:

Field **Group_permissions.id**
==============================





Type: AutoField

   
.. index::
   single: field;group
   
.. _igen.auth.Group_permissions.group:

Field **Group_permissions.group**
=================================





Type: ForeignKey

   
.. index::
   single: field;permission
   
.. _igen.auth.Group_permissions.permission:

Field **Group_permissions.permission**
======================================





Type: ForeignKey

   


.. index::
   pair: model; Group

.. _igen.auth.Group:

---------------
Model **Group**
---------------



Groups are a generic way of categorizing users to apply permissions, or some other label, to those users. A user can belong to any number of groups.

    A user in a group automatically has all the permissions granted to that group. For example, if the group Site editors has the permission can_edit_home_page, any user in that group will have that permission.

    Beyond permissions, groups are a convenient way to categorize users to apply some label, or extended functionality, to them. For example, you could create a group 'Special users', and you could write code that would do special things to those users -- such as giving them access to a members-only portion of your site, or sending them members-only e-mail messages.
    
  
==== ========= ============
name type      verbose name
==== ========= ============
id   AutoField ID          
name CharField name        
==== ========= ============

    
Defined in :srcref:`/django/contrib/auth/models.py`

.. index::
   single: field;id
   
.. _igen.auth.Group.id:

Field **Group.id**
==================





Type: AutoField

   
.. index::
   single: field;name
   
.. _igen.auth.Group.name:

Field **Group.name**
====================





Type: CharField

   


.. index::
   pair: model; User_user_permissions

.. _igen.auth.User_user_permissions:

-------------------------------
Model **User_user_permissions**
-------------------------------



User_user_permissions(id, user_id, permission_id)
  
========== ========== ===============
name       type       verbose name   
========== ========== ===============
id         AutoField  ID             
user       ForeignKey user (Benutzer)
permission ForeignKey permission     
========== ========== ===============

    
Defined in :srcref:`/django/contrib/auth/models.py`

.. index::
   single: field;id
   
.. _igen.auth.User_user_permissions.id:

Field **User_user_permissions.id**
==================================





Type: AutoField

   
.. index::
   single: field;user
   
.. _igen.auth.User_user_permissions.user:

Field **User_user_permissions.user**
====================================





Type: ForeignKey

   
.. index::
   single: field;permission
   
.. _igen.auth.User_user_permissions.permission:

Field **User_user_permissions.permission**
==========================================





Type: ForeignKey

   


.. index::
   pair: model; User_groups

.. _igen.auth.User_groups:

---------------------
Model **User_groups**
---------------------



User_groups(id, user_id, group_id)
  
===== ========== ===============
name  type       verbose name   
===== ========== ===============
id    AutoField  ID             
user  ForeignKey user (Benutzer)
group ForeignKey group          
===== ========== ===============

    
Defined in :srcref:`/django/contrib/auth/models.py`

.. index::
   single: field;id
   
.. _igen.auth.User_groups.id:

Field **User_groups.id**
========================





Type: AutoField

   
.. index::
   single: field;user
   
.. _igen.auth.User_groups.user:

Field **User_groups.user**
==========================





Type: ForeignKey

   
.. index::
   single: field;group
   
.. _igen.auth.User_groups.group:

Field **User_groups.group**
===========================





Type: ForeignKey

   


.. index::
   pair: model; User

.. _igen.auth.User:

--------------
Model **User**
--------------




Users within the Django authentication system are represented by this model.

Username and password are required. Other fields are optional.

  
============ ============= ================
name         type          verbose name    
============ ============= ================
id           AutoField     ID              
username     CharField     username        
first_name   CharField     first name      
last_name    CharField     last name       
email        EmailField    e-mail address  
password     CharField     password        
is_staff     BooleanField  staff status    
is_active    BooleanField  active          
is_superuser BooleanField  superuser status
last_login   DateTimeField last login      
date_joined  DateTimeField date joined     
============ ============= ================

    
Defined in :srcref:`/django/contrib/auth/models.py`

.. index::
   single: field;id
   
.. _igen.auth.User.id:

Field **User.id**
=================





Type: AutoField

   
.. index::
   single: field;username
   
.. _igen.auth.User.username:

Field **User.username**
=======================



Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters

Type: CharField

   
.. index::
   single: field;first_name
   
.. _igen.auth.User.first_name:

Field **User.first_name**
=========================





Type: CharField

   
.. index::
   single: field;last_name
   
.. _igen.auth.User.last_name:

Field **User.last_name**
========================





Type: CharField

   
.. index::
   single: field;email
   
.. _igen.auth.User.email:

Field **User.email**
====================





Type: EmailField

   
.. index::
   single: field;password
   
.. _igen.auth.User.password:

Field **User.password**
=======================



Use '[algo]$[salt]$[hexdigest]' or use the <a href="password/">change password form</a>.

Type: CharField

   
.. index::
   single: field;is_staff
   
.. _igen.auth.User.is_staff:

Field **User.is_staff**
=======================



Designates whether the user can log into this admin site.

Type: BooleanField

   
.. index::
   single: field;is_active
   
.. _igen.auth.User.is_active:

Field **User.is_active**
========================



Designates whether this user should be treated as active. Unselect this instead of deleting accounts.

Type: BooleanField

   
.. index::
   single: field;is_superuser
   
.. _igen.auth.User.is_superuser:

Field **User.is_superuser**
===========================



Designates that this user has all permissions without explicitly assigning them.

Type: BooleanField

   
.. index::
   single: field;last_login
   
.. _igen.auth.User.last_login:

Field **User.last_login**
=========================





Type: DateTimeField

   
.. index::
   single: field;date_joined
   
.. _igen.auth.User.date_joined:

Field **User.date_joined**
==========================





Type: DateTimeField

   


.. index::
   pair: model; Message

.. _igen.auth.Message:

-----------------
Model **Message**
-----------------




The message system is a lightweight way to queue messages for given
users. A message is associated with a User instance (so it is only
applicable for registered users). There's no concept of expiration or
timestamps. Messages are created by the Django admin after successful
actions. For example, "The poll Foo was created successfully." is a
message.

  
======= ========== ===============
name    type       verbose name   
======= ========== ===============
id      AutoField  ID             
user    ForeignKey user (Benutzer)
message TextField  message        
======= ========== ===============

    
Defined in :srcref:`/django/contrib/auth/models.py`

.. index::
   single: field;id
   
.. _igen.auth.Message.id:

Field **Message.id**
====================





Type: AutoField

   
.. index::
   single: field;user
   
.. _igen.auth.Message.user:

Field **Message.user**
======================





Type: ForeignKey

   
.. index::
   single: field;message
   
.. _igen.auth.Message.message:

Field **Message.message**
=========================





Type: TextField

   


