====
auth
====



.. currentmodule:: auth

Defined in :srcref:`/lino/modlib/auth/models.py`


This is a stripped copy of `django.contrib.auth`.




.. index::
   pair: model; Permission
   single: field;id
   single: field;name
   single: field;content_type
   single: field;codename

.. _igen.auth.Permission:

--------------------
Model ``Permission``
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
   pair: model; Group_permissions
   single: field;id
   single: field;group
   single: field;permission

.. _igen.auth.Group_permissions:

---------------------------
Model ``Group_permissions``
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
   pair: model; Group
   single: field;id
   single: field;name

.. _igen.auth.Group:

---------------
Model ``Group``
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
   pair: model; User_user_permissions
   single: field;id
   single: field;user
   single: field;permission

.. _igen.auth.User_user_permissions:

-------------------------------
Model ``User_user_permissions``
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
   pair: model; User_groups
   single: field;id
   single: field;user
   single: field;group

.. _igen.auth.User_groups:

---------------------
Model ``User_groups``
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
   pair: model; User
   single: field;id
   single: field;username
   single: field;first_name
   single: field;last_name
   single: field;email
   single: field;password
   single: field;is_staff
   single: field;is_active
   single: field;is_superuser
   single: field;last_login
   single: field;date_joined

.. _igen.auth.User:

--------------
Model ``User``
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
   pair: model; Message
   single: field;id
   single: field;user
   single: field;message

.. _igen.auth.Message:

-----------------
Model ``Message``
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


