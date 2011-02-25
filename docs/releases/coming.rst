Coming
======

#.  Der Button "Auskunftsblatt" ist provisorisch raus.


Upgrade instructions
--------------------

- In your local :xfile:`settings.py`, replace the line

  ::

    #~ from lino.demos.dsbe.settings import *
  
  with
  
  ::
  
    from lino.sites.dsbe.settings import *


- Go to your local directory::

    cd /usr/local/django/myproject
    
- Stop application services::

    ./stop
    
- Update the source code::

    ./pull
    
- When a data migration is necessary, see :doc:`/admin/datamig`

