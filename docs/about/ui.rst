==================
The user interface
==================

People tend to judge a framework by it's user interface (UI). 
This approach is not completely wrong since the UI is the first "visible" part.
But Lino is designed to have many possible user interfaces,
it comes with an extensible collection of **out-of-the-box user interfaces**
because we believe that application developers should *develop applications*
and should not waste their time writing html templates or css.

That said, we admit that your choice is currently 
limited to the :term:`ExtJS` UI [#f1]_.
This means that Lino applications currently always 
"look like" those you can see at :doc:`/demos`.


Some important general elements of every Lino user interface are

- the main menu : a hierarchical representation of the 
  application's functions. 
  In multi-user applications the main menu heavily changes 
  depending on the user profile.

- Sophistacated Grids to display tabular data

- Tabbed form input for detail windows.

- ComboBoxes with dynamic data store.

- Context-sensitive ComboBoxes

- Keyboard navigation for areas are where manual data entry is needed.

- WYSIWYG rich text editor

- Unlike some desktop applications does *not* reimplement 
  an internal method to open several windows:
  users simply open several browser windows.







.. rubric:: Footnotes

.. [#f1] We started working on a first alternative user interface 
  that uses the :doc:`Qooxdoo library </topics/qooxdoo>`,
  and we can imagine to write other interfaces in the future 
  (simple HTML, curses, Qt, ...), but for the moment 
  Lino relies on ExtJS, because ExtJS is so cool, 
  and because writing and optimizing a user interface 
  is a rather boring work, 
  and because there are many other, 
  more interesting tasks that are waiting to be done.

