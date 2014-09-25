The values behind Lino
======================

In this text Luc tries to explain what Lino *really* means to him,
why he loves his work and believes that it is worth doing it.

The Lino framework is born from my wish to promote peace between two
long-term ennemies called "developers" and "end-users" by breaking
down walls and building bridges.


Linked objects
--------------

"Lino" is an acronym of the words "**Lin**\ ked **o**\ bjects".

Every software application has a "model" of its "world", i.e. of the
things which it is designed to manage.  We call this a database
schema. Such a schema mainly consists of "objects" and the "relations"
or "links" between them. The idea of using *linked objects* for this
modelization has been first formulated by Edgar F. Codd in 1969 in his
`relational database model
<https://en.wikipedia.org/wiki/Relational_model>`_.

But even 50 years later this idea is still some kind of expert
knowledge, known to database engineers but not to normal people.
Since the early 1990s I have often observed that application
developers seem to hide from the end-users the fact that their
application is basically "nothing but a collection of linked objects".
As if they were ashamed to admit that what they are doing is *that*
easy.

**Yes, a Lino application *is* that easy.** They feature a transparent
view of their database schema, leading to end-users being intuitively
aware of the structure behind what they are doing.  One Lino
application developer who understood this, wrote: "The development is
so terribly easy, that one customer looked at the code and started to
code Layouts and modify models by himself and I almost felt no
developer is needed anymore :-)"

**No, there is no reason to be ashamed.** We continue to need
professional developers because the gory details require some
experience, and because it is an art to make the right choices on what
to take into account and what to ignore.
  
The IT world is suffering from developers who are very competent but
unable to communicate with end-users.  This is where specialization
becomes absurd, because a software application makes no sense without
its users.

- When end-users are intuitively aware of the structure behind what
  they are doing, this leads to better communication between
  developers and end-users because **they speak the same language**.
  (Well that's an exaggeration -- it's normal that there are certain
  differences in vocabulary, but:) They stop to completely miss the
  point of what the other is talking about.

- Lino applications give their users a **feeling of being able** to do
  it themselves.  This motivates them to start thinking about how they
  actually *would* do it themselves.  The developer then just
  implements what they ask, no more need to translate their language
  or to analyze their "true needs", because the users understand what
  is possible and correctly analyze what they really need.


Lino is a common first name in Italy
------------------------------------

Yes, I wanted **a human name** for our framework.
Lino makes it possible to write complex applications that are like 
children: they grow day by day, 
giving parental joy to those who collaborate to their development.
See also :doc:`name`.



