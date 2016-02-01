=================
Lino and Python 3
=================

Lino currently still needs Python 2. Adding support for Python 3
(:ticket:`36`) is one of our goals for 2016. We are working on it.
You can help us.

First you need to create a virtualenv under Python 3.

Method 1 (Hamza)
================

- Update the server::

    $ apt-get update

- Install pip3::

    $ sudo apt-get install pip3

- Install virtualenv via pip::

    $ pip3 install virtualenv

- Make a new virtual environment::

    $ cd ~/virtualenvs
    $ virtualenv py3

- Activate the new virtual environment::

    $ source py3/bin/activate

Method 2 (Ubuntu)
=================

::

    $ sudo apt-get install python3
    $ cd ~/virtualenvs
    $ virtualenv -p python3 py3
    
