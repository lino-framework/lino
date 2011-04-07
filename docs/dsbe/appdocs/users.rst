=====
users
=====



.. currentmodule:: users

Defined in :srcref:`/lino/modlib/users/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; User

.. _std.users.User:

--------------
Model **User**
--------------




Represents a User of this site.

This version of the Users table is used on Lino sites with
:doc:`/topics/http_auth`. 

Only username is required. Other fields are optional.

There is no password field since Lino is not responsible for authentication.
New users are automatically created in this table when 
Lino gets a first request with a username that doesn't yet exist.
It is up to the local system administrator to manually fill then 
fields like first_name, last_name, email, access rights for the new user.    

  
============ ============= ================
name         type          verbose name    
============ ============= ================
id           AutoField     ID              
username     CharField     username        
first_name   CharField     first name      
last_name    CharField     last name       
email        EmailField    e-mail address  
is_staff     BooleanField  staff status    
is_active    BooleanField  active          
is_superuser BooleanField  superuser status
last_login   DateTimeField last login      
date_joined  DateTimeField date joined     
============ ============= ================

    
Defined in :srcref:`/lino/modlib/users/models.py`

.. index::
   single: field;id
   
.. _std.users.User.id:

Field **User.id**
=================





Type: AutoField

   
.. index::
   single: field;username
   
.. _std.users.User.username:

Field **User.username**
=======================




        Required. 30 characters or fewer. 
        Letters, numbers and @/./+/-/_ characters
        

Type: CharField

   
.. index::
   single: field;first_name
   
.. _std.users.User.first_name:

Field **User.first_name**
=========================





Type: CharField

   
.. index::
   single: field;last_name
   
.. _std.users.User.last_name:

Field **User.last_name**
========================





Type: CharField

   
.. index::
   single: field;email
   
.. _std.users.User.email:

Field **User.email**
====================





Type: EmailField

   
.. index::
   single: field;is_staff
   
.. _std.users.User.is_staff:

Field **User.is_staff**
=======================




        Designates whether the user can log into this admin site.
        

Type: BooleanField

   
.. index::
   single: field;is_active
   
.. _std.users.User.is_active:

Field **User.is_active**
========================




        Designates whether this user should be treated as active. 
        Unselect this instead of deleting accounts.
        

Type: BooleanField

   
.. index::
   single: field;is_superuser
   
.. _std.users.User.is_superuser:

Field **User.is_superuser**
===========================




        Designates that this user has all permissions without 
        explicitly assigning them.
        

Type: BooleanField

   
.. index::
   single: field;last_login
   
.. _std.users.User.last_login:

Field **User.last_login**
=========================





Type: DateTimeField

   
.. index::
   single: field;date_joined
   
.. _std.users.User.date_joined:

Field **User.date_joined**
==========================





Type: DateTimeField

   


