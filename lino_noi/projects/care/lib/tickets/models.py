from lino_noi.lib.tickets.models import *
from lino.api import _

Ticket.hide_elements('closed')


class TicketDetail(TicketDetail):
    main = "general more history_tab"

    general = dd.Panel("""
    general1:60 faculties.AssignableWorkersByTicket:20
    comments.CommentsByRFC:60 clocking.SessionsByTicket:20
    """, label=_("General"))

    general1 = """
    summary:40 id:6
    reporter:12 faculty topic assigned_to
    site project private workflow_buttons
    """


Tickets.detail_layout = TicketDetail()
