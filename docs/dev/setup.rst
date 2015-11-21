.. _dev.setup_info:

========================
How Lino uses `setup.py`
========================

The :xfile:`setup_info.py` file is a trick which does not depend on
Lino and which I recommend to use for any Python project.

Usually the setup information is directly contained in a file
:xfile:`setup.py` in the root directory of a project. The problem with
this layout is that this :xfile:`setup.py` file is not always
available at runtime (depending on how Lino was installed).

To solve this problem, I store this information in a separate file
(which I usually name :xfile:`setup_info.py`) and which I execute from
both my :xfile:`setup.py` and my packages's :xfile:`__init__.py` file.
This trick makes it possible to have setup information both in a
central place **and** accessible at runtime.


.. xfile:: setup_info.py

    The file which contains the information for Python's `setup.py`
    script, e.g. the Lino **version number** or the **dependencies**
    (i.e. which other Python packages must be installed when using
    Lino).

So that's why Lino's :xfile:`setup.py` contains just this::

    from setuptools import setup
    execfile('lino/setup_info.py')
    if __name__ == '__main__':
        setup(**SETUP_INFO)
    
And the :file:`lino/__init__.py` file contains a line like this::
    
    execfile(join(dirname(__file__), 'setup_info.py'))

Usage example:

>>> import lino
>>> print lino.SETUP_INFO['description']
A framework for writing desktop-like web applications using Django and ExtJS

