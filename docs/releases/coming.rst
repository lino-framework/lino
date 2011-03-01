Coming
======

#.  Der Button "Auskunftsblatt" ist provisorisch raus.

#.  Database migration needed because:
    - New field :attr:`lino.modlib.properties.PropType.default_value`

Upgrade instructions
--------------------

- In your templates, change calls to `tr()` by `babelattr()`.
  tr is now an alias for babelitem.

- changes in your local :xfile:`settings.py`

  - Replace the line

    ::

      from lino.demos.dsbe.settings import *
    
    by
    
    ::
    
      from lino.sites.dsbe.settings import *
      
  - Replace the settings
  
    ::
      
      LANGUAGE_CODE = "de"
      BABEL_LANGS = ['fr','en']
      
    by
      
    ::
      
      LANGUAGE_CODE = "de"
      LANGUAGES = language_choices('de','fr','en')

    
  


- Go to your local directory::

    cd /usr/local/django/myproject
    
- Stop application services::

    ./stop
    
- Update the source code::

    ./pull
    python manage.py test dsbe
    
  Note: 
  For some apps the tests are currently broken. 
  That's just because we didn't yet find time to maintain them.
  We're working on it.

    
- When a data migration is necessary, see :doc:`/admin/datamig`

