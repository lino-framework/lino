Names, labels, and titles
=========================

A name is *internal* (usable in Python code) 
and identifies the actor in its module's 
namespace (the app_label).
Users usually don't see the name of an actor. 
Except for example in a permalink.

The label and the title of an actor both are descriptive 
strings presented to the user. The label is shorter than the title. 
The label is used when the actor has not yet opened, for example on a 
button or menu item that *will* open this actor.

Both label and title of a model table default to 
Django's `verbose_name_plural`.

The class 
:class:`lino.utils.babel.BabelNamed`
should one day be renamed to 
:class:`lino.utils.babel.BabelLabeled`,
and (less easy because it will cause much 
code for the data migration) have a field `label` instead of `name`.