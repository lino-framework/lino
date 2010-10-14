"""
:mod:`dsbe.demo`
================

This is a `Django project <http://docs.djangoproject.com/en/dev/intro/tutorial01/#creating-a-project>`__ 
just to have a quick out-of-the-box demo and a template for your own DSBE installatino which will be outside 
of the DSBE source trunk.

Besides the normal Django files
(:xfile:`urls.py`, :xfile:`manage.py`, :xfile:`settings.py`)
it contains a file :xfile:`lino_settings.py` 
and some scripts which should probably become Django manage commands:

.. xfile:: load_tim.py

Import data from TIM.

.. xfile:: tim2lino.py

Synchronize changes from TIM to Lino.




"""