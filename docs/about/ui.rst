.. _lino.ui:

==================
The user interface
==================

People tend to judge a framework by it's user interface (UI).  This
approach is not completely wrong since the UI is the first "visible"
part.  But Lino is designed to have many possible user interfaces. 

Separate business logic and user interface
==========================================

Lino comes with an extensible collection of **out-of-the-box user
interfaces** because we believe that application developers should
*develop applications* and should not waste their time writing html
templates or css.  It is one of Lino's design goals to separate
business logic and user interface.

You write a Lino application once, and then you can "deploy" (or use
it yourself) via many different interfaces. For example

- a more lightweight web interface using some other JS framework than ExtJS
- a web interface optimized for read-only access and publication of
  complex data (something like :ref:`belref`, but we agree that this
  needs more work before becoming really usable)
- a console UI using `ncurses <https://en.wikipedia.org/wiki/Ncurses>`_
- We once started working on an interface that uses the :doc:`Qooxdoo
  library </topics/qooxdoo>`.
- a desktop application using `Qt
  <https://en.wikipedia.org/wiki/Qt_%28software%29>`_ or `wxWidgets
  <https://en.wikipedia.org/wiki/WxWidgets>`_
- an XML or JSON based HTTP interface
- one might consider Lino's :class:`TextRenderer
  <lino.core.renderer.TextRenderer>` (used for writing tested
  functional specifications like `this one
  <http://welfare.lino-framework.org/specs/households.html>`_) as a
  special kind of user interface.

That said, we admit that in practice, your choice is currently limited
to the :term:`ExtJS` UI.  Lino applications currently "look like"
those you can see at :doc:`/demos`.

That's because ExtJS is so cool, and because writing and optimizing a
user interface is a rather boring work, and because there are many
other, more interesting tasks that are waiting to be done.

The first serious alternative UI will be the new ExtJS6 interface. We
are working on it (:ticket:`37`).

Elements of a user interface
============================

It is not enough to say that you want to separate "business logic" and
"user interface". The question is *where exactly* you are going to
separate.  The actual challenge is the API between them.

Lino has a rather high-level API because we target a rather wide range
of possible interfaces.

That API is still evolving and not yet very well documented, but the
basics seem to have stabilized.  Some general elements of every Lino
user interface are:

- the main menu : a hierarchical representation of the 
  application's functions. 
  In multi-user applications the main menu heavily changes 
  depending on the user profile.

- sophistacated grids to display tabular data

- Tabbed form input for detail windows.

- ComboBoxes with dynamic data store.

- Context-sensitive ComboBoxes.

- Keyboard navigation for areas are where manual data entry is needed.

- WYSIWYG rich text editor

- Support for multi-lingual database content

- Unlike some desktop applications Lino does *not* reimplement an
  internal method to open several windows: users simply open several
  browser windows.


TODO: Answer to comments in `this discussion on twitter
<https://twitter.com/LucSaffre/status/716809890489049088>`_ where
Christophe asks "il ne suffit pas juste d'un format d'échange
clairement spécifié?"  and SISalp comments "On ne parle pas de la même
chose. Dans Flask + Tryton, l'application Flask fait "import trytond"
et ça change tout.  See also :ref:`tryton`.
