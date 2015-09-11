==============
Things to know
==============

A list of things you should know as a :doc:`/team/lad`
before you can start to love Lino.


Python
======

Lino is mostly written in the Python programming language. You know
for example

- what's an object, a string, a list, a dict, a float
- the difference between a class method and an instance method
- what's a generator
- what's a decorator
- what are the following standard modules used for:
  `datetime`,  `sys`,  `os`, `re`,  `decimal`,  `logging`, ... 
- the major differences between Python 2 and 3

Django
======

Lino applications are Django projects.

- You know how to get a Django project up and running.
  (You should have followed the `Tutorial <https://docs.djangoproject.com/en/dev/>`_)
  You know what a :xfile:`settings.py` file is.
- You know most about Django's model layer : the ``Model`` class,
  the field types, executing database queries


Git
===

Lino is hosted on Github. You know how to use this collaboration
platform.

- You have read the `GitHub Help <https://help.github.com>`_ pages,
  especially the "Bootcamp" and "Setup" sections.
- You have created a free account on GitHub and made a fork of Lino.
- You are able to make some change in your working copy, commit your
  branch and send a pull request.


Sphinx
======

Documentation about Lino is written using `Sphinx
<http://sphinx-doc.org>`_.

- You should know how Sphinx works and why we use it. Important chapters of
  the Sphinx documentation include
  `The build configuration file <http://sphinx-doc.org/config.html>`_

- You should try to use the same blogging system as Luc and to document
  your own contributions to Lino in a :doc:`developer blog
  </team/devblog>`.  


The UNIX shell
==============

Lino is a web application framework. You are going to install it on
web servers. Free people use free operating systems.

- You know the meaning of shell commands like ``ls``, ``cp``, ``rm``,
  ``cd``, ``ls``
- You have written your own bash scripts. You know how to use shell
  variables and functions.
- You know what is a pipe, what is redirection
- You can configure your bash and know about the files :file:`.bashrc`
  and :file:`.bash_aliases`.


HTML, CSS and Javascript
========================

- You understand the meaning of tags like 
  ``<body>``, ``<ul>``, ``<li>`` ...
- You understand how Lino uses the Sencha ExtJS Javascript library
- You know what an AJAX request is.

Databases
=========

Lino is a part of Django and therefore uses relational databases
(SQL). You don't often need to write SQL yourself when using Lino, but
it is of course important to understand the concepts behind a
database. And on a production server you will have to deal with
database servers like MySQL or PostgreSQL (according to the
:setting:`DATABASES` setting).

