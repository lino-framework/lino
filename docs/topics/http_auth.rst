HTTP authentication
===================

HTTP authentication is currently the only method supported 
by Lino (because there hasn't been any need for other methods 
until now).

The thing to keep in mind with HTTP authentication is that Lino   
delegates the authentication to the web server.

Concretely this means that Lino trusts completely the REMOTE_USER 
header of any incoming request. 
If there is no user with that username in Lino's database, 
Lino will silently create a User with minimum rights. 

There is currently no system (yet) to automatically synchronize 
Lino's Users table from the LDAP server or whatever user database 
used by the web server.

User-specific rights management is not yet very stable in Lino. 
For example there's no concept of user groups for the moment.

Lino does not need any sessions in such a configuration.

See also

- :doc:`/tickets/31`
- :mod:`lino.modlib.users`