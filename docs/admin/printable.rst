==============================
Generating printable documents
==============================

This page is about the old and complex topic of 
generating **printable documents** out of a database application, 
using some type of **templates**.

Lino comes with a selection 
of ready-to-use *production chains* for this task, which we call
**build methods**.



Vocabulary
==========

**Printable documents** are files in one of the following formats:

- .pdf
- .ps
- .odt
- .doc or .rtf

Printable documents may be either **editable** (.odt, .doc, .rtf) or **non-editable** (.pdf, .ps).

Printable documents may be **delivered** (1) either to the end-user who will view them
and possibly print them out on her printer, or (2) sent directly from the application server 
to a printer in a local area network.

**Templates** are files managed by a local site administrator that serve as *master documents* 
into which Lino will insert data from the database.

Templates are either **WYSIWYG** (.odt, .rtf) or **Markup** (.html, .tex).


Build methods
=============

.. currentmodule:: lino.mixins.printable

Here is an overview of the build methods implemented (or planned) in Lino.

  +-----------------------------+------------+---------+----------------------------+----------------------------+
  | build method                | template   | output  | Parser                     | Post-processor             |
  |                             | filename   | filename|                            |                            |
  |                             | format     | format  |                            |                            |
  +=============================+============+=========+============================+============================+
  | :class:`AppyBuildMethod`    | .odt       | .odt    |  :term:`appy_pod`          |  -                         |
  +-----------------------------+------------+---------+----------------------------+----------------------------+
  | :class:`AppyDocBuildMethod` | .odt       | .doc    |  :term:`appy_pod`          |  OOo server                |
  +-----------------------------+------------+---------+----------------------------+----------------------------+
  | :class:`AppyPdfBuildMethod` | .odt       | .pdf    |  :term:`appy_pod`          |  OOo server                |
  +-----------------------------+------------+---------+----------------------------+----------------------------+
  | :class:`RtfBuildMethod`     | .rtf       | .rtf    |  :term:`pyratemp`          |  -                         |
  +-----------------------------+------------+---------+----------------------------+----------------------------+
  | :class:`LatexBuildMethod`   | .tex       | .pdf    |  Django/Jinja              |  pdfLaTeX                  |
  +-----------------------------+------------+---------+----------------------------+----------------------------+
  | :class:`PisaBuildMethod`    | .pisa.html | .pdf    |  Django/Jinja              |  :term:`Pisa`              |
  +-----------------------------+------------+---------+----------------------------+----------------------------+
                                                                                             

Template engines
================

A `template engine <http://en.wikipedia.org/wiki/Template_engine_(web)>`_ 
is responsible for replacing *template commands* by their result.
The template engine determines the syntax for specifying template 
commands when designing templates.

- :class:`PisaBuildMethod` and :class:`LatexBuildMethod` use 
  `Django's template engine
  <http://docs.djangoproject.com/en/dev/topics/templates/>`_ whose 
  template commands look for example like 
  ``{% if instance.has_family %}yes{% else %}no{% endif %}``
  or
  ``My name is {{ instance.name }}.``.
  


- Appy/Pod (:class:`AppyBuildMethod` & Co) uses a special approach: 
  it marks template commands 
  using OOo's "change records" and "comments" features. 
  Appy/Pod also handles transparently 
  the fact that .odt files are in fact .zip files containing a set of .xml files.

- :class:`RtfBuildMethod` uses :term:`pyratemp` as template engine 
  whose template commands looks like ``@!instance.name!@``.
  We cannot use Django's template engine because 
  both use curly braces as command delimiters.
  
  This build method has a flaw: I did not find a way to 
  "protect" the template commands in your RTF files from being formatted by Word.
  
Markup versus WYSIWYG
=====================

Template collections that use some markup language are usually 
less redundant because 
you can design your collection intelligently by using template inheritance.

On the other hand, maintaining a collection of markup templates 
requires a relatively skilled person because the maintainer must 
know two "languages": the template engine's syntax and the markup syntax.

WYSIWYG templates (OpenOffice or Word) increase the probability 
that an end-user is able to maintain the template collection because 
there's only on language to learn (the template engine's syntax)



Post-processing
===============

Some print methods need post-processing: the result of parsing must be 
run through another piece software in order to turn into a usable format.
Post-processing creates dependencies to other software and has of 
course influence on runtime performance.


Pisa vs. LaTeX
==============

- Pisa uses less server resources at runtime than LaTeX.

- You can include Pisa into your project, while LaTeX is a separate
  software with its own package management to be installed.
  
- Creating .html templates from existing .odt or .doc files 
  is easier than creating .tex templates.
  There is html2latex but I have no real-world experience with it.
    
- Pisa is rather limited, while LaTeX is 
  rather unlimited, well-documented and stable.
  

Not yet implemented
===================

There are some other possible candidates that we didn't yet have time to meet with:

- `rst2pdf <http://rst2pdf.googlecode.com>`_
  is a tool to convert restructured text to PDF using reportlab.

- `wkhtmltopdf <http://code.google.com/p/wkhtmltopdf>`_.
  converts html to pdf using the webkit rendering engine, and qt.
  There is also a `Python binding <http://github.com/mreiferson/py-wkhtmltox>`_
  
- `RTF Template <http://rtftemplate.sourceforge.net/>`_ uses another approach: 
  users design their templates by "using merge fields (MERGEFIELD), 
  hyperlink fields (HYPERLINK) and 
  bookmarks (BOOKMARK, to manage start/end loop)."
  

Weblinks
========

.. glossary::

  appy_pod
    http://appyframework.org/pod.html
    
  Pisa
    http://www.xhtml2pdf.com/
    HTML/CSS to PDF converter written in Python.
    See also :doc:`/blog/2010/1020`
    
  odtwriter
    http://www.rexx.com/~dkuhlman/odtwriter.html
    http://www.linuxbeacon.com/doku.php?id=articles:odfwriter
  
  pyratemp
    http://www.simple-is-better.org/template/pyratemp.html


