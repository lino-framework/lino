# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models of `lino.modlib.addresses`.

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino.utils.xmlgen.html import E
from lino.core.utils import ChangeWatcher

from .choicelists import AddressTypes


class AddressOwner(dd.Model):
    """Base class for the "addressee" of any address.

    """
    class Meta:
        abstract = True

    def get_address_by_type(self, address_type):
        Address = rt.modules.addresses.Address
        try:
            return rt.modules.addresses.Address.objects.get(
                partner=self, address_type=address_type)
        except Address.DoesNotExist:
            return self.get_primary_address()
        except Address.MultipleObjectsReturned:
            return self.get_primary_address()
        
    def get_primary_address(self):
        Address = rt.modules.addresses.Address
        # AddressTypes = rt.modules.addresses.AddressTypes
        # ADDRESS_FIELDS = rt.modules.addresses.ADDRESS_FIELDS

        kw = dict(partner=self, primary=True)
        try:
            return Address.objects.get(**kw)
        except Address.DoesNotExist:
            kw.update(address_type=AddressTypes.official)
            has_values = False
            for fldname in Address.ADDRESS_FIELDS:
                v = getattr(self, fldname)
                kw[fldname] = v
                if v:
                    has_values = True
            if has_values:
                addr = Address(**kw)
                addr.full_clean()
                addr.save()
                return addr

    def get_overview_elems(self, ar):
        elems = super(AddressOwner, self).get_overview_elems(ar)
        sar = ar.spawn('addresses.AddressesByPartner',
                       master_instance=self)
        # btn = sar.as_button(_("Manage addresses"), icon_name="wrench")
        btn = sar.as_button(_("Manage addresses"))
        # elems.append(E.p(btn, align="right"))
        elems.append(E.p(btn))
        return elems
    
    def sync_primary_address(self, request):
        Address = rt.modules.addresses.Address
        watcher = ChangeWatcher(self)
        kw = dict(partner=self, primary=True)
        try:
            pa = Address.objects.get(**kw)
            for k in Address.ADDRESS_FIELDS:
                setattr(self, k, getattr(pa, k))
        except Address.DoesNotExist:
            pa = None
            for k in Address.ADDRESS_FIELDS:
                fld = self._meta.get_field(k)
                setattr(self, k, fld.get_default())
        self.save()
        watcher.send_update(request)


