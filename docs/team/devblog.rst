.. _devblog:

=============================
Start your own developer blog
=============================

This section explains what a **developer blog** is, why you need it,
and how you do it.

Documenting what you do
=======================

The daily work of a software developer includes things like modifying
source code, pushing changes to public repositories, writing comments
in forums, surfing around, reading books, discovering new
technologies, contributing to other projects... 

The basic idea of a developer blog is that you **leave a trace** about
what you have been doing, and that this trace is in a **central
place**.

In your developer blog you simply describe what you are doing. Day by
day. Using plain English language. It is your diary.  

A developer blog **does not need** to be cool, popular or easy to
follow.  It **should rather be**:

- *complete* (e.g. not forget to mention any important code
  change you did) and 
- *concise* (use references to point to places where the reader can
  continue if they are interested).
- *understandable* at least for yourself and for other team members. 

Your blog is a diary, but keep in mind that it is **public**. The
usual rules apply: don't disclose any passwords or private data.
Respect other people's privacy.  Don't quote other author's words
without naming them. Always reference your sources of information.


You probably know already one example of a developer blog, namely
`Luc's developer blog <http://luc.lino-framework.org>`_.

We suggest that you start blogging like this.  You may of course use
another system, especially if you have been blogging before.  The
important thing is that you report about your daily work in order to
share your experiences, your know-how, your successes, your mistakes
and your stumblings.


Luc's blogging system
=====================

Luc's "developer blog" is free, simple and extensible.  It is based on
`Sphinx <http://sphinx-doc.org/>`_ which is the established standard
for Python projects.  It answers well to certain requirements which we
perceive as important:

- A developer uses some editor for writing code, and wants to use that
  same editor for writing his blog.

- A developer usually works on more than one software projects at a
  time.

- A developer should not be locked just because there is no internet
  connection available for a few hours.

As a new new team member, once you've got used to this system, this
can be the easiest way to ask for help in complex cases which need
screenshots, links, sections etc.

The developer blog fits into our collaboration workflow: the :cmd:`fab
ci` command knows where your developer blog is and generates a commit
message which points to today's blog entry.

"Blog" versus "Documentation tree"
==================================

Luc's blogging system uses *daily* entries (maximum one blog entry per
day), and is part of some Sphinx documentation tree.

So don't mix up "a blog" with "a documentation tree".  You will
probably maintain only one *developer blog*, but you will maintain
many different *documentation trees*.  Not every documentation tree
contains a blog.

You probably will soon have other documentation trees than the one
which contains your blog. For example your first Lino application
might have a local project name "hello", and it might have two
documentation trees, one in English (`hello/docs`) and another in
Spanish (`hello/docs_es`). `fab pd` would upload them to
`public_html/hello_docs` and `public_html/hello_docs_es` respectively.
See :attr:`env.docs_rsync_dest <atelier.fablib.env.docs_rsync_dest>`.


.. _dblog:

The `dblog` project template
============================

To help you get started with blogging in your own developer blog,
there is a project template at https://github.com/lsaffre/dblog


How to configure your blog
==========================

You may find inspiration from the Lino website for configuring your
developer blog.

- Interesting files are:
  :file:`/docs/conf.py`
  :file:`/docs/.templates/layout.html`
  :file:`/docs/.templates/links.html`
