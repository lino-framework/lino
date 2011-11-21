#coding: latin1


from lino.schemas.sprl.demo import getDemoDB
from lino.adamo.twisted_ui import webserver

db = getDemoDB(isTemporary=True,populator=None)

def page(**kw):
	return db.PAGES.appendRow(**kw)

def populate():
	db.installto(globals())

	home = page(
		match="index",
		title='The Lino Database Application Framework',
		abstract="""

Welcome to the Lino homepage.

- `Overview <overview>`_
  
- `Frequently asked questions <faq>`_

- `Lino diary <news>`_

- `Installing <install>`_ Lino.

- `Getting started <start>`_ with Lino.

- `Links <links>`_


Here are some tests:
[ref PARTNERS:1 First Partner],
[ref MSX:1 Home],
[url http://lino.sf.net Lino].

		
		""",body="""

		[url ORGS Links]


		""")

	overview = page(title="Overview",
						 super=home,
						 match="overview",
						 abstract="""
Lino is a framework for IT professionals who offer integrated business
applications for small and medium-sized enterprises.
							 """,
						 body="""
Lino is published under the GNU General Public License (GPL) and
implemented as a suite of Python packages.  Although these packages
could possibly be useful separately, they are designed to co-operate.

I started to publish Lino as a Sourceforge project in August 2003.
Lino is currently rather a sandbox for several modules in different
states of development and with different degrees of co-operation.  The
only thing that they have in common is that I am author and
maintainer.


- `WebMan <webman>`_ is yet another system to create web pages. It
  is used to generate this Website.
  
- `Python Document Script <pds/index.html>`_ (PDS) is a reporting
  system to generate static documents on screen or paper.

- `TIM tools <timtools>`_ are a collection of command-line
  tools designed as helpers for DOS applications.
  
Being developed:


- `Adamo <adamo>`_ ("abstract data model") is an API for writing
  database schemas in pure Python, including business logic and
  validation rules.
   
- agui (abstract user interface model) : adds forms, dialogs and menus
  to a database.

- The `Web UI <wui.html>`_ is a standalone HTTP server which runs a
  Web Application that gives access to an Adamo database.
   
- Lino comes with a collection of reusable and interconnectible
  application components

							 
   """)
							 
							 

	faq = page(title="Overview",
				  super=home,
				  match="faq",
				  abstract="""
				  """,
				  body="""

.. contents:: Table of Contents


How many developers are working on the project?
-----------------------------------------------

I am alone. For the moment.
Project author and currently only developer is Luc Saffre who works
for Rumma & Ko.  Rumma & Ko is a service provider in Tallinn with 2
employees.  They live currently by selling support for `TIM
<http://my.tele2.ee/lsaffre/tim>`_.  Lino is one of their long-term
future projects.


What is the project's status?
-----------------------------

(this entry last updated 2003-10-04)

- The `Web UI <wui.html>`_
  is currently most active.
  
- The `TIM tools <timtools.html>`_ are being used by some of my
  customers.
  
- The sdoc module currently can generate HTML and PDF. The HTML part
  is currently not used and will perhaps even vanish.
  
- `Adamo <adamo.html>`_
  is already quite beautiful, but only in theory.
  Adamo is now waiting for the `Web UI <wui.html>`_.

- Documentation, including this web site is work in progress.


Why did you start your own project?
-----------------------------------

"I have been writing customized database applications for over 10
years. I am tired of looking for the perfect framework.  Now I am
going to write it myself!"

Of course the question remains active: am I re-inventing the wheel?
This is why I maintain my `Links <links.html>`_ page which evolves
each time I am pondering with this question.

        "There is a certain charm to seeing someone happily advocate a
        triangular wheel because it has one less bump per revolution
        than a square wheel does. (Chuck Swiger)"

        "Someone, somewhere said that you should at least skim through
        the standard library of the language of your choice, just
        because you shouldn't be re-inventing the wheel all the
        time. (But don't underestimate the value of re-inventing the
        wheel."  (Jarno Virtanen)

Lino is an experimental project.  It is possible that parts of it are
going to vanish completely if appropriate existing software solutions
can be used.



Why the name "Lino"?
--------------------

There is no serious reason.  Consider "Lino" just as a
personalization.  Do you remember `Lino Ventura
<http://www.allocine.fr/personne/fichepersonne_gen_cpersonne=400.html>`_
?  I like to give human names to my software projects because they are
in many respects like a person to me.

But originally is "Lino" an acronym for "Linked Objects".  I used this
name in 1990 for a (never-published) tool to visualize the "Links" and
"Objects" of a datamodel defined for a proprietary database server.
The tool has gone, but the name remained in my head.

Afterwards I realized that "Lino" could be interpreted as "Lucs
Increasingly Never-ending Obsessions"...

				  """)

	PAGES.appendRow(
		match="impressum",
		super=home,
		title="Impressum",
		abstract="""
		Diese Website ist ein Prototyp.
		""", body="""
		Ich weiß selber, dass noch viel daran zu tun ist,
		aber freue mich über Rückmeldungen und Verbesserungsideen.

		Luc Saffre.
		
		"""
		)

	from lino.misc import bullshit
	PAGES.appendRow(
		match=None,
		super=home,
		title="Bullshit Bingo",
		abstract=bullshit.abstract(),body=bullshit.body())



## 	PAGES.appendRow(
## 		match=None,
## 		super=home,
## 		title="",
## 		abstract="""
## 		""", body="""
## 		"""
## 		)




	db.commit()
	

populate()

webserver(db,port=8080,staticDirs={
	'files': 'files',
	'images': 'images',
	'thumbnails': 'thumbnails'
	}, showOutput=False)
