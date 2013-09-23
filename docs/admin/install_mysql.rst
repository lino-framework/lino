Use a MySQL database
--------------------

If you decided to use MySQL as database frontend, 
then here is a cheat sheet for quickly doing so.
(No warranty.)

To install mysql on your site::

    $ sudo aptitude install mysql-server python-mysqldb
    
Or if your site is to run within a virtualenv::
    
    $ sudo aptitude install mysql-server libmysqlclient-dev python-dev
    $ pip install MySQL-python
    
For your first project create a user ``django`` which you can 
reuse for all projects::
    
    $ mysql -u root -p 
    mysql> create user 'django'@'localhost' identified by 'my cool password';
    
For each new project you must create a database and grant permissions 
to ``django``::
    
    $ mysql -u root -p 
    mysql> create database mysite charset 'utf8';
    mysql> grant all on mysite.* to django with grant option;
    mysql> grant all on test_mysite.* to django with grant option;
    mysql> quit;
    
    
    
See also http://dev.mysql.com/doc/refman/5.0/en/charset-database.html

And then of course you set DATABASES in your :xfile:`settings.py` 
file::

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'mysite',                      # Or path to database file if using sqlite3.
            # The following settings are not used with sqlite3:
            'USER': 'django',
            'PASSWORD': 'my cool password',
            'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',                      # Set to empty string for default.
        }
    }


