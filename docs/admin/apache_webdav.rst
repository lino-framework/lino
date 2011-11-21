Installing a WebDAV section
===========================

Lino expects that files below `/media/webdav/` are served 
using the WebDAV protocol. 
The client's computer should automatically launch OpenOffice or MS-Word to open them.


- `How To Set Up WebDAV With Apache2 On Debian Etch <http://www.howtoforge.com/setting-up-webdav-with-apache2-on-debian-etch>`_

To allow WebDAV, add another `<Directory>` directive::
  
  <Directory /usr/local/django/myproject/media/webdav/>
     DAV On
     ForceType text/plain
     AuthType Basic
     AuthName "Lino/DSBE demo"
     AuthUserFile /usr/local/django/myproject/htpasswd/passwords
     AuthGroupFile /usr/local/django/myproject/htpasswd/groups
     <LimitExcept GET>
     Require group dav
     </LimitExcept>
  </Directory>

Maybe also ``a2enmod dav_fs`` 




http://www.howtoforge.com/setting-up-webdav-with-apache2-on-debian-etch