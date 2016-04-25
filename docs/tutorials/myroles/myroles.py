from lino.modlib.polls.roles import *

from lino.api import dd, rt
t = rt.modules.polls.AllPolls
t.required_roles = dd.login_required(PollsUser)
