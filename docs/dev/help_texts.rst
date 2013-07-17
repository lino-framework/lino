.. _help_texts:

Help Texts
==========

Help texts are defined 

- by application code using 
  :attr:`lino.core.actors.Actor.help_text`
  or
  :attr:`lino.core.actions.Action.help_text`
- by the users using 
  :class:`HelpText <lino..modlib.system.models.HelpText>`
  
Note that the standard user interface displays them only when 
:attr:`lino.ui.Site.use_quicklinks` must be `True`.
