## Copyright 2011-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
The name ``dd`` stands for "Data Dictionary". 

See :class:`lino.core.table.Table` etc.

"""


from lino.utils.tables import VirtualTable
#~ from lino.utils.tables import computed
#~ from lino.utils.tables import ComputedColumn

from lino.tools import resolve_model, get_app, resolve_field

from lino.core.table import fields_list, inject_field
from lino.core.table import has_fk
from lino.core.table import Table
#~ from lino.core import table
#~ Table = table.Table

from lino.core.table import summary, summary_row

from lino.core.actors import Frame
from lino.core.actors import EmptyTable

from lino.core.actions import RowAction
from lino.core.actions import GridEdit, ShowDetailAction
from lino.core.actions import InsertRow, DeleteSelected
from lino.core.actions import SubmitDetail, SubmitInsert
from lino.core.actions import Calendar

from lino.core.fields import GenericForeignKey
from lino.core.fields import GenericForeignKeyIdField
from lino.core.fields import IncompleteDateField
from lino.core.fields import DisplayField
from lino.core.fields import VirtualField
from lino.core.fields import displayfield, virtualfield
from lino.core.fields import PasswordField
from lino.core.fields import MonthField
from lino.core.fields import LinkedForeignKey
from lino.core.fields import QuantityField
from lino.core.fields import HtmlBox, PriceField, RichTextField
from lino.core.fields import RequestField, requestfield
from lino.core.fields import Constant
from lino.core.fields import constant
#~ from lino.core.fields import MethodField

from lino.utils import perms

from lino.core.layouts import DetailLayout


class Module(object):
    pass