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

In your developer blog you simply describe what you are doing. You
report about your daily work in order to share your experiences, your
know-how, your successes, your mistakes and your stumblings.  Day by
day. Using plain English language. It is your diary.

The basic idea of a developer blog is that you **leave a trace** about
what you have been doing, and that this trace is in a **central
place**.

A developer blog **does not need** to be cool, exciting, popular or
easy to follow.  It **should rather be**:

- *complete* (e.g. not forget to mention any important code
  change you did) and 
- *concise* (use references to point to places where the reader can
  continue if they are interested).
- *understandable* at least for yourself and for other team members. 

Your blog is a diary, but keep in mind that it is **public**. The
usual rules apply: don't disclose any passwords or private data.
Respect other people's privacy.  Don't quote other author's words
without naming them. Always reference your sources of information.

A developer blog can be the easiest way to ask for help in
complex cases which need screenshots, links, sections etc.

Our collaboration workflow 
The developer blog fits into
the :cmd:`fab ci` command knows where your
developer blog is and generates a commit message which points to
today's blog entry.


Luc's blogging system
=====================

You probably know already one example of a developer blog, namely
`Luc's developer blog <http://luc.lino-framework.org>`_.  The
remaining sections describe how you can use Luc's system for your own
blog.

You may of course use another blogging system (blogger.com,
wordpress.com etc,), especially if you have been blogging before.

Luc's developer blog is free, simple and extensible.  
It answers well to certain requirements which we perceive as
important:

- A developer uses some editor for writing code, and wants to use that
  same editor for writing his blog.

- A developer usually works on more than one software projects at a
  time.

- A developer should not be locked just because there is no internet
  connection available for a few hours.

It is based on `Sphinx <http://sphinx-doc.org/>`_ which is the
established standard for Python projects. This has the advantage that
your blog has the same syntax as your docstrings.

It does *not* have a way for followers to "subscribe". This is because
they can subscribe to your commits to your code repositories anyway,
and because there are monitoring tools which they can use to get
notified when your blog changes (e.g. `5 Free Tools To Notify You of
Website Content Changes
<http://www.hongkiat.com/blog/detect-website-change-notification/>`__)


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


.. You may find inspiration from the Lino website for configuring your
   developer blog.

    - Interesting files are:
      :file:`/docs/conf.py`
      :file:`/docs/.templates/layout.html`
      :file:`/docs/.templates/links.html`
