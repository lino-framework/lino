.. _belref:

=====================
The Belgian Reference
=====================

Lino Belref is a website with various "structured" information 
about Belgium in three national languages.
An early prototype is running at http://belref.lino-framework.org
and is mentioned on our :ref:`demos` page.

The official primary goal of this project is rather ambitious:
provide a new way for storing, maintaining and publishing 
certain kind of **structured data** 
(our example currently shows a dictionary with specific "Belgian" 
vocabulary and a database of Belgian cities and other geographic 
names, but even that choice is just illustrative and not a definitive decision).
The system would -among others- automatically maintain a new 
class of **generated Wikipedia pages**.

The data on such a site would be **stored** as :ref:`dpy`
which makes it possible to 
maintain the content using established development tools for
version control, issue tracking and testing.
This mixture of data and source code is currently 
published and maintained as part part of Lino's repository 
in the :mod:`lino.projects.belref` package.

The project grows **very slowly** because I know no 
single person who believes that this might make sense
(besides myself of course, but even I wouldn't give my hand for it).

A side effect with potentially more concrete impact is that this 
is also our test field for the 
new light-weight user interface for Lino
(see :ref:`plain`).





