Configure Apache for HTTP authentication
========================================

Here is how I configured Apache using basic HTTP authentication for the demo sites. 
In a production site you'll of course use more secure authentication methods.
My source was http://httpd.apache.org/docs/2.0/howto/auth.html.

Create a local directory for the flatfile user database::

  # mkdir /usr/local/lino/htpasswd

Create a first user::

  # htpasswd -c /usr/local/lino/htpasswd/passwords root

Create more users::

  # htpasswd /usr/local/lino/htpasswd/passwords user


Create a groups file :file:`nano/usr/local/lino/htpasswd/groups` with the following content::

  lino: root user

Then, in your Apache config file (:file:`/etc/apache2/sites-available/default`)::

  <Directory />
    AuthType Basic
    AuthName "Lino demo"
    AuthUserFile /usr/local/lino/htpasswd/passwords
    AuthGroupFile /usr/local/lino/htpasswd/groups
    Require group demo
  </Directory>
