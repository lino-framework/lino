from lino.utils.appy_pod import PrintTableAction, PortraitPrintTableAction
from lino.core.tables import AbstractTable
AbstractTable.as_pdf = PrintTableAction()
AbstractTable.as_pdf_p = PortraitPrintTableAction()
