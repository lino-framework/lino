Authentication
==============

HTTP authentication
-------------------

HTTP authentication is currently the only method supported 
by Lino (because there hasn't been any need for other methods 
until now).

This means basically that Lino delegates the authentication to the web server.
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
    (feature used by e.g. :mod:`lino.test_apps.1`)
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





