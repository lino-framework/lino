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
from lino.mixins.repairable import Repairable

from .choicelists import AddressTypes


class AddressOwner(Repairable):
    """Base class for the "addressee" of any address.

    """
    class Meta:
        abstract = True

    def get_address_by_type(self, address_type):
        Address = rt.modules.addresses.Address
        try:
            return Address.objects.get(
                partner=self, address_type=address_type)
        except Address.DoesNotExist:
            return self.get_primary_address()
        except Address.MultipleObjectsReturned:
            return self.get_primary_address()

    def get_primary_address(self, update=False):
        """Return the primary address of this partner.

        If the optional argument `update` is True, this method has a
        side effect of updating or even creating an address record
        when appropriate and possible:

        - if there is exactly one :class:`Address` object which just fails to
          be marked as primary, mark it as primary and return it.

        - if there is no :class:`Address` object, and if the
          :class:`Partner` has some non-empty address field, create an
          address record from these, using `AddressTypes.official` as
          type.

        """
        Address = rt.modules.addresses.Address

        kw = dict(partner=self, primary=True)
        try:
            return Address.objects.get(**kw)
        except Address.DoesNotExist:
            pass
        qs = Address.objects.filter(partner=self)
        num = qs.count()
        if num == 1:
            addr = qs[0]
            if update:
                addr.primary = True
                addr.full_clean()
                addr.save()
            return addr
        elif num == 0 and update:
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

    def repairdata(self, really=False):
        yield super(AddressOwner, self).repairdata(really)
        # TODO

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

    def get_overview_elems(self, ar):
        elems = super(AddressOwner, self).get_overview_elems(ar)
        sar = ar.spawn('addresses.AddressesByPartner',
                       master_instance=self)
        # btn = sar.as_button(_("Manage addresses"), icon_name="wrench")
        btn = sar.as_button(_("Manage addresses"))
        # elems.append(E.p(btn, align="right"))
        elems.append(E.p(btn))
        return elems
    
