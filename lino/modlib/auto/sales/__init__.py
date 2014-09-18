# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

#from lino import ad

from lino.modlib.sales import Plugin


class Plugin(Plugin):

    extends_models = ['Invoice',  'InvoiceItem']
