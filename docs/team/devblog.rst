.. _devblog:

=====================
About developer blogs
=====================

A **developer blog** is a blog with daily entries (maximum one blog entry
per day), which is part of some `Sphinx <http://sphinx-doc.org/>`_
documentation tree.

This way of blogging was developed and is used by :ref:`luc`.  We
recommend that you also start your own developer blog.


Documenting what you do
=======================

The basic idea of a developer blog is that you should document
"everything you do" in a central place.

A developer uses some editor for writing code, and wants to use that
same editor for writing his blog.

A developer usually works on more than one software projects at a
time, modifying source code, pushing changes to public repositories,
writing comments in forums, surfing around and discovering new
knowledge.

A developer should not be locked just because there is no internet
connection available for a few hours.

What should I write into my developer's blog?
=============================================

You describe what you are doing.  It is your diary.

A developer blog should be understandable at least for yourself and
for other team members. It *doesn't need* to be cool, popular, easy to
follow. It should rather be *complete* (e.g. not forget to mention any
important code change you did) and *concise* (use references to point
to places where the reader can continue if they are interested).

For example, Luc's developer blog is currently part of the Lino
documentation tree (see :ref:`blog`). That's because Luc is currently
the main contributor of Lino. One day we might decide to split Luc's
blog out of the Lino repo into a separate repository.

Don't mix up "a blog" with "a documentation tree".  You will probably
maintain only one *blog*, but you will maintain many different
*documentation trees*. Not every documentation tree contains a blog.

You probably will soon have other documentation trees. For example
your first Lino application might have a local project name "hello",
and it might have two documentation trees, one in English
(`hello/docs`) and another in Spanish (`hello/docs_es`). `fab pd`
would upload them to `public_html/hello_docs` and
`public_html/hello_docs_es` respectively.  See
:attr:`env.docs_rsync_dest <atelier.fablib.env.docs_rsync_dest>`.


Why?
====

We don't know whether Luc's system is better than other systems, but
we recommend to use so that we have a coherent system within the team.
It is free, simple and extensible.  It is based on `Sphinx
<http://sphinx-doc.org/>`_ which is the established standard for
Python projects.

As a new new team member, once you've got used to this system, this
will be the easiest way for the other members to follow what you are
doing, where you are stumbling, where you need help.

The developer blog is also part or our collaboration workflow: the
:cmd:`fab ci` command knows where your developer blog is and generates
a commit message which points to today's blog entry.


.. _dblog:

The `dblog` project template
============================

To help you get started with blogging in your own developer blog,
there is a project template at https://github.com/lsaffre/dblog

