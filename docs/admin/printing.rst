========
Printing
========

Lino uses :class:`print methods <lino.utils.printable.PrintMethod>` to address the old and 
complex topic of generating digital documents out of a database application.

.. currentmodule:: lino.utils.printable

Here is an overview of the print methods implemented (or planned) in Lino.

  +-----------------------------+------------+---------+---------+----------------------------+----------------------------+
  | print method                | template   | output  | WYSIWYG | Parser                     | Post-processor             |
  |                             | filename   | filename| or      |                            |                            |
  |                             | format     | format  | Markup  |                            |                            |
  +=============================+============+=========+=========+============================+============================+
  | :class:`AppyPrintMethod`    | .odt       | .odt    | WYSIWYG |  :term:`appy`              |  -                         |
  +-----------------------------+------------+---------+---------+----------------------------+----------------------------+
  | :class:`AppyDocPrintMethod` | .odt       | .doc    | WYSIWYG |  :term:`appy`              |  OOo server                |
  +-----------------------------+------------+---------+---------+----------------------------+----------------------------+
  | :class:`AppyPdfPrintMethod` | .odt       | .pdf    | WYSIWYG |  :term:`appy`              |  OOo server                |
  +-----------------------------+------------+---------+---------+----------------------------+----------------------------+
  | :class:`RtfPrintMethod`     | .rtf       | .rtf    | WYSIWYG |  rtfparse (to be written)  |  -                         |
  +-----------------------------+------------+---------+---------+----------------------------+----------------------------+
  | :class:`LatexPrintMethod`   | .tex       | .pdf    | Markup  |  Django/Jinja              |  pdfLaTeX                  |
  +-----------------------------+------------+---------+---------+----------------------------+----------------------------+
  | :class:`PisaPrintMethod`    | .pisa.html | .pdf    | Markup  |  Django/Jinja              |  :term:`Pisa`              |
  +-----------------------------+------------+---------+---------+----------------------------+----------------------------+
                                                                                             

Markup versus WYSIWYG
=====================

Template collections that use some markup language are usually less redundant because 
you can design your collection intelligently by using template inheritance.

On the other hand, maintaining a collection of markup templates 
requires a relatively skilled person. 
WYSIWYG templates (OpenOffice or Word) increase the probability 
that an end-user is able to maintain the template collection.

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
  

Other possible candidates might be 
`rst2pdf <http://code.google.com/p/rst2pdf/>`_
and
`wkhtmltopdf <http://code.google.com/p/wkhtmltopdf>`_.


Template engines
================

A `template engine <http://en.wikipedia.org/wiki/Template_engine_(web)>` 
means to replace *template commands* by their result.

The template engine determines the syntax for specifying template 
commands when designing templates.

For markup templates we can simply use `Django's templating system 
<http://docs.djangoproject.com/en/dev/topics/templates/>`_  as parser.

For WYSIWYG templates the topic is more complex.

Most parsers expect template commands to be surrounded by delimiters. 
For example angle brackets (``<...>``) or combined patterns like ``{{...}}``.

- Appy/Pod uses a special approach: it marks template commands 
  using OOo's "change record" feature. Appy/Pod also handles transparently 
  the fact that .odt files are in fact .zip files containing a set of .xml files.

- For the RTF format we cannot use the Django template parser because 
  both use curly braces as command delimiters.

  I once wrote my own parser that uses square brackets (``[...]``) 
  as command delimiters. This method has a flaw: I did not find a way to 
  "protect" the template commands in your RTF files from being formatted by Word.
  
  `RTF Template <http://rtftemplate.sourceforge.net/>`_ uses another approach: 
  users design their templates by "using merge fields (MERGEFIELD), 
  hyperlink fields (HYPERLINK) and 
  bookmarks (BOOKMARK, to manage start/end loop)."
  
Post-processing
===============

Some print methods need post-processing: the result of parsing must be 
run through another piece software in order to turn into a usable format.

