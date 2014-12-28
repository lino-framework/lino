.. _devblog:

========================
What is a Develope blog?
========================

Every team member keeps his or her developer blog.
We recommend to use :ref:`luc`\ 's system, which we are going to
introduce here.

A developer blog is a blog with daily entries (maximum one blog entry
per day) and written using the `Sphinx documentation generator
<http://sphinx-doc.org/>`_.

The basic idea is that everything you do should be documented in your
devblog.  A developer blog should be understandable at least for
yourself and for other team members.

Each developer usually works on more than one software projects, but
usually maintains only one devblog.

Luc's developer blog is currently included in the Lino documentation
tree (below :ref:`blog`) because Luc is currently the main author of
Lino.

As a new new team member, once you've got used to this system, this
will be the easiest way for the other members to follow what you are
doing, where you are stumbling, where you need help.

The developer blog is also part or our collaboration workflow: the
:cmd:`fab ci` command knows where your developer blog is and generates
a commit message which points to today's blog entry.


Note that one developer usually maintains only one *blog*, but can
maintain many different *Sphinx documentation trees*. Not every
documentation tree contains a blog.

You probably will soon have other documentation trees. For example
your first Lino application might have a local project name "hello",
and it might have two documentation trees, one in English
(`hello/docs`) and another in Spanish (`hello/docs_es`). `fab pd`
would upload them to `public_html/hello_docs` and
`public_html/hello_docs_es` respectively.

See :attr:`env.docs_rsync_dest <atelier.fablib.env.docs_rsync_dest>`.
This mapping is not
configurable, and I currently don't think that it would be a good idea
to make it configurable.




.. _dblog:

The `dblog` project template
============================

To help you get started with blogging in your own developer blog,
there is a project template at https://github.com/lsaffre/dblog

