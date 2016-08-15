from lino_noi.lib.tickets.models import *
from lino.api import _

Ticket.hide_elements('closed')


class Ticket(Ticket):
    class Meta(Ticket.Meta):
        app_label = 'tickets'
        verbose_name = _("Plea")
        verbose_name_plural = _("Pleas")
        abstract = dd.is_abstract_model(__name__, 'Ticket')

ActiveTickets._label = _("Active pleas")
UnassignedTickets._label = _("Unassigned pleas")
PublicTickets._label = _("Public pleas")
TicketsToTriage._label = _("Pleas to triage")
TicketsToTalk._label = _("Pleas to talk")
TicketsToDo._label = _("Pleas to to")
TicketsFixed._label = _("Fixed pleas")
TicketsReported._label = _("Introduced pleas")
TicketsByReporter._label = _("Introduced pleas")

dd.update_field(
    'tickets.Ticket', 'upgrade_notes', verbose_name=_("Solution"))


class TicketDetail(TicketDetail):
    main = "general more history_tab"

    general = dd.Panel("""
    general1:60 faculties.AssignableWorkersByTicket:20
    comments.CommentsByRFC:60 clocking.SessionsByTicket:20
    """, label=_("General"))

    general1 = """
    summary:40 id:6
    reporter:12 faculty topic assigned_to
    deadline site project #private workflow_buttons
    """

    more = dd.Panel("""
    more1
    description:40 upgrade_notes:20 LinksByTicket:20
    """, label=_("More"))

    more1 = """
    created modified ticket_type:10
    state priority
    # standby feedback closed
    """



Tickets.detail_layout = TicketDetail()
