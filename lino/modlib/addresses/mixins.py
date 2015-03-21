# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Model mixins for `lino.modlib.addresses`.

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext_lazy as _

from lino.api import rt, dd
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
            return Address.objects.get(
                partner=self, address_type=address_type)
        except Address.DoesNotExist:
            return self.get_primary_address()
        except Address.MultipleObjectsReturned:
            return self.get_primary_address()

    def get_primary_address(self):
        """Return the primary address of this partner.

        """
        Address = rt.modules.addresses.Address
        try:
            return Address.objects.get(partner=self, primary=True)
        except Address.DoesNotExist:
            pass

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
    
from lino.modlib.plausibility.choicelists import Checker


class AddressOwnerChecker(Checker):
    """Checks for the following plausibility problems:

    - :message:`Unique address is not marked primary.` --
      if there is exactly one :class:`Address` object which just fails to
      be marked as primary, mark it as primary and return it.

    - :message:`Non-empty address fields, but no address record.`
      -- if there is no :class:`Address` object, and if the
      :class:`Partner` has some non-empty address field, create an
      address record from these, using `AddressTypes.official` as
      type.

    """
    verbose_name = _("Check for missing or non-primary address records")
    model = AddressOwner
    
    def get_plausibility_problems(self, obj, fix=False):
        Address = rt.modules.addresses.Address
        qs = Address.objects.filter(partner=obj)
        num = qs.count()
        kw = dict()
        for fldname in Address.ADDRESS_FIELDS:
            v = getattr(obj, fldname)
            if v:
                kw[fldname] = v
        if num > 1:
            return
        if num == 1:
            addr = qs[0]
            if not addr.primary:
                # check whether it is the same address than the one
                # specified on AddressOwner
                diff = {}
                for k, other in kw.items():
                    my = getattr(addr, k)
                    if my != other:
                        diff[k] = (my, other)
                if len(diff) == 0:
                    yield (True, _("Unique address is not marked primary."))
                    if fix:
                        addr.primary = True
                        addr.full_clean()
                        addr.save()
                    return
                # else:
                #     dd.logger.info("20150321, diff is %s", diff)
                    
        if kw:
            yield (True,
                   _("Non-empty address fields, but no address record."))
            if fix:
                kw.update(partner=obj, primary=True)
                kw.update(address_type=AddressTypes.official)
                addr = Address(**kw)
                addr.full_clean()
                addr.save()

AddressOwnerChecker.activate()
