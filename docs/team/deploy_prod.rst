.. _team.deploy_prod:

===========================
Deploy to a production site
===========================

The server has two subdomains "lino" and "testlino". Each subdomain
has its own project directory. Each project directory has a symbolic
link `env` which points to its Python environment.

- Create a new virtualenv::

    $ cd ~/pythonenvs
    $ virtualenv b

  Clone the code repositories and install them into the new environment::

    $ cd ~/pythonenvs/b
    $ mkdir repositories
    $ cd repositories

    $ git clone https://github.com/lsaffre/lino.git
    $ git clone https://github.com/lsaffre/lino-cosi.git
    $ git clone https://github.com/lsaffre/lino-welfare.git

    $ pip install -e lino
    $ pip install -e lino-cosi
    $ pip install -e lino-welfare
    
  Install the Python binding for MySQL::
    
    pip install MySQL-python


- Check whether a snapshot exists

- Compare the :xfile:`settings.py` files::

      $ cd /usr/local/django/prod
      $ diff settings.py ../testing/settings.py

  Most differences are normal, but the new version might require
  changes. Normal differences:

  - The Django settings :setting:`ALLOWED_HOSTS`,  :setting:`DATABASES`
    :setting:`ADMINS`

  - Plugin settings like
    :attr:`cbss_environment <lino_welfare.modlib.cbss.Plugin.cbss_environment>`
    :attr:`cbss_live_requests <lino_welfare.modlib.cbss.Plugin.cbss_live_requests>`

- Switch the project directories to their new environments::

    $ cd /usr/local/django/prod
    $ ls -ld env
    lrwxrwxrwx 1 lsaffre www-data 33 Sep 28 18:54 env -> /home/luc/pythonenvs/a
    $ rm env
    $ ln ~/pythonenvs/b env
    $ ls -ld env
    lrwxrwxrwx 1 lsaffre www-data 33 Sep 28 18:54 env -> /home/luc/pythonenvs/b

  Usually every project moves to the "next" environment.

- Run `collectstatic` in the new environment::

    $ cd /usr/local/django/testing
    $ a
    $ python manage.py collectstatic
    ...
    You have requested to collect static files at the destination
    location as specified in your settings:

        /home/lsaffre/pythonenvs/b/collectstatic

    This will overwrite existing files!
    Are you sure you want to do this?
    
  Note that we define the :setting:`STATIC_ROOT` in both project
  dirs as follows::
    
    STATIC_ROOT = SITE.project_dir.child('env', 'collectstatic').resolve()

  Note that `project_dir` is a `Unipath
  <https://github.com/mikeorr/Unipath>`_ object, and that the `resolve
  <https://github.com/mikeorr/Unipath#calculating-paths>`_ method
  resolves symbolic links (transforms them to their "real" path).

- Restore production data from snapshot::

    $ cd /usr/local/django/prod
    $ a
    $ python manage.py run snapshot/restore.py 

- Restart Apache

- Log in and see whether everything seems okay.

