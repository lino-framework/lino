Authentication
==============

Lino applications must decide which 
*authentication and permission system* to use:

- Django's `django.contrib.auth
  <https://docs.djangoproject.com/en/dev/topics/auth/>`_ 
  module
- Lino's own system using UserLevels, UserGroups and UserProfiles


  

The :xfile:`settings.py` file decides which authentication method to use:

- If :attr:`user_model <lino.Lino.user_model>` is `None`, 
  there's no authentication and request.user is always 
  an :class:`lino.utils.auth.AnonymousUser` instance.
  
Otherwise, :attr:`user_model <lino.Lino.user_model>` 
can be either 'users.User' or 'auth.User'. 
In both cases we have two more possibilities:

- If :attr:`lino.Lino.remote_user_header` 
  contains some value, your application will use 
  `HTTP authentication`_
  
- If :attr:`lino.Lino.remote_user_header` is `None`, 
  your application uses `Session-based authentication`_

Session-based authentication
----------------------------

This means that your application 
has the "Login", "Logout" and "Register" buttons
and `django.contrib.sessions` to your INSTALLED_APPS.

This behaviour is automatically activated when 
:attr:`lino.Lino.remote_user_header` is `None` 
(and :attr:`lino.Lino.user_model` not).



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
(:attr:`lino.Lino.remote_user_header`) 
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

Even though Lino currently supports only remote authentication,
there *is* an application-specific table of users managed by Lino.
The default Model, :class:`lino.modlib.users.models.User`
For each request, Lino will lookup this table




    user_model = "users.User"
    """Set this to ``"auth.User"`` if you use `django.contrib.auth` instead of
    `lino.modlib.users`. 
    
    Set it to `None` to remove any user management 
    (feature used by e.g. :mod:`lino.test_apps.mti`)
    """
    
    default_user = None
    """
    Username to be used if a request with 
    no REMOTE_USER header makes its way through to Lino. 
    Which may happen on a development server and if Apache is 
    configured to allow it.
    Used by :mod:`lino.utils.auth`
    :mod:`lino.modlib.users.middleware`
    """
    
    remote_user_header = "REMOTE_USER"
    """
    The name of the header (set by the web server) that Lino consults 
    for finding the user of a request.
    """
    #~ simulate_remote_user = False
    
    project_model = None
    """Optionally set this to the <applabel_modelname> of a 
    model used as project in your application."""





