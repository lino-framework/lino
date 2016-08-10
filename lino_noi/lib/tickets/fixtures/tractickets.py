import codecs
import datetime
from unipath import Path
from atelier.utils import AttrDict
from lino.api import rt

fn = Path(__file__).parent.child('tractickets.tsv')
# http://trac.lino-framework.org/query?status=accepted&status=assigned&status=closed&status=new&status=reopened&col=id&col=summary&col=status&col=owner&col=type&col=priority&col=milestone&col=component&col=severity&col=resolution&col=time&col=changetime&col=reporter&order=id


COLUMNS = """id summary status owner type priority milestone
component severity resolution time changetime reporter""".split()


def makeuser(username):
    User = rt.modules.users.User
    u, created = User.objects.get_or_create(username=username.strip())
    if created:
        # u.profile = rt.modules.users.UserProfiles.admin
        # u.set_password('1234')
        # u.modified = datetime.datetime.now()
        u.full_clean()
        u.save()
    return u


def objects():
    Project = rt.modules.tickets.Project
    Milestone = rt.models.deploy.Milestone
    Ticket = rt.modules.tickets.Ticket
    User = rt.modules.users.User
    TicketStates = rt.modules.tickets.TicketStates

    states = set()

    for n, row in enumerate(codecs.open(fn, encoding="utf-8").readlines()):
        if n == 0:
            continue  # headers
        if not row:
            continue
        cells = row.split('\t')
        if len(cells) != len(COLUMNS):
            msg = "Oops, line {0} has {1} cells".format(n, len(cells))
            raise Exception(msg)
        d = AttrDict()
        for i, k in enumerate(COLUMNS):
            d.define(k, cells[i])
        kw = dict()
        kw.update(id=d.id)
        kw.update(summary=d.summary)
        if d.reporter:
            kw.update(reporter=makeuser(d.reporter))
        else:
            kw.update(reporter=makeuser('luc'))
        if d.owner:
            kw.update(
                assigned_to=makeuser(d.owner))
        if d.component:
            prj = Project.objects.get_or_create(ref=d.component)[0]
        else:
            prj = Project.objects.get_or_create(ref='etc')[0]
        kw.update(project=prj)
        if d.milestone:
            mls = Milestone.objects.get_or_create(
                project=prj, label=d.milestone)[0]
            kw.update(fixed_for=mls)
            kw.update(state=TicketStates.done)
        elif d.status == ('closed'):
            kw.update(state=TicketStates.done)
        elif d.status in ('assigned', 'accepted'):
            kw.update(state=TicketStates.active)
        else:
            kw.update(state=TicketStates.get_by_name(d.status))
        # if d.resolution == 'fixed':
        # else:
        #     raise Exception("Invalid resolution {0}".format(d.resolution))
        kw.update(created=d.time)
        kw.update(modified=d.changetime)
        states.add(d.status)
        yield Ticket(**kw)
    # print states




# # http://trac-hacks.org/wiki/XmlRpcPlugin#PythonEnd-UserUsage

# import xmlrpclib

# from lino.api import dd

# server = xmlrpclib.ServerProxy(dd.plugins.lino_noi.trac_url)
         
# multicall = xmlrpclib.MultiCall(server)
# for ticket in server.ticket.query("owner=luc"):
#     multicall.ticket.get(ticket)

# print map(str, multicall())
