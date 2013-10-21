Authentication
==============



Lino defines some configuration settings for easily switching 
between different commonly-used authentication methods.
In other words, 
Lino automatically decides which authentication method to 
use and installs the required middleware
depending on your :xfile:`settings.py` file.

You may override these out-of-the-box methods by 
specifying the :setting:`auth_middleware` setting. 
If this is not empty, the logic described here does not apply.

- If :setting:`user_model` is `None`, 
  there's no authentication and `request.user` is always 
  an :class:`AnonymousUser <lino.core.perms.AnonymousUser>` instance.
  
Otherwise, :setting:`user_model` 
can be either 'users.User' or 'auth.User' (the latter is not tested). 
In both cases we have two more possibilities:

- If :setting:`remote_user_header` 
  contains some value, your application will use 
  `HTTP authentication`_
  
- If :setting:`remote_user_header` is `None`, 
  your application uses `Session-based authentication`_

Session-based authentication
----------------------------

This means that your application
has "Login", "Logout" and "Register" buttons,
and that `django.contrib.sessions` is added to your INSTALLED_APPS.

There are two variants of session-based authentication:

- If :setting:`ldap_auth_server` is `None`, Lino uses the passwords 
  stored in its own database.

- If :setting:`ldap_auth_server` is not `None`, Lino authenticates 
  against the specified LDAP server.


HTTP authentication
-------------------

`HTTP authentication 
<http://en.wikipedia.org/wiki/Basic_access_authentication>`_ 
means basically that Lino delegates the authentication 
to the web server.

This method suits best when there is already 
a central user management system (e.g. an LDAP server)
running on a site and authentication granted by the web server.

Lino trusts completely the 
`REMOTE_USER` header 
(:attr:`remote_user_header <lino.ui.Site.remote_user_header>`) 
of any incoming request. 
If there is no user with that username in Lino's database, 
Lino will silently create a User with minimum rights. 

There is currently no system (yet) to automatically synchronize 
Lino's Users table from the LDAP server or whatever user database 
used by the web server.

One advantage of this is that Lino does not need any sessions.


See also

- :doc:`/tickets/31`
- :mod:`lino.modlib.users`
- :doc:`/admin/ApacheHttpAuth`

