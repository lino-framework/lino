======================
Multilingual databases
======================

One of Lino's key features is 
:doc:`support for multilingual database content  </topics/babel>`.
This tutorial tries to explain what it is.

Note: If you have a :doc:`lino_local </admin/lino_local>` 
directory with your 
:attr:`extjs_root <lino.Lino.extjs_root>` defined, 
then you can run directly from the Lino source repository::

  cd ~/snapshots/lino/lino/apps/babel_tutorial
  mkdir media
  python manage.py testserver demo

The `media` directory must exist, otherwise the 
development server won't populate it.




:xfile:`settings.py`

.. literalinclude:: ../../lino/apps/babel_tutorial/settings.py

Depending on the 


:xfile:`models.py`

.. literalinclude:: ../../lino/apps/babel_tutorial/models.py

:xfile:`models.py`

.. literalinclude:: ../../lino/apps/babel_tutorial/fixtures/demo.py
