# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Model mixins for `lino.modlib.addresses`.

"""

from __future__ import unicode_literals
from __future__ import print_function
from builtins import object

from django.utils.translation import ugettext_lazy as _

from lino.api import rt, dd
from lino.utils.xmlgen.html import E
from lino.core.utils import ChangeWatcher
from lino.modlib.plausibility.choicelists import Checker

from .choicelists import AddressTypes


class AddressOwner(dd.Model):
    """Base class for the "addressee" of any address.

    """
    class Meta(object):
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
        watcher = ChangeWatcher(self)
        self.sync_primary_address_()
        watcher.send_update(request)

    def sync_primary_address_(self):
        Address = rt.modules.addresses.Address
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

    def get_overview_elems(self, ar):
        if ar is None:
            return []
        elems = super(AddressOwner, self).get_overview_elems(ar)
        sar = ar.spawn('addresses.AddressesByPartner',
                       master_instance=self)
        # btn = sar.as_button(_("Manage addresses"), icon_name="wrench")
        btn = sar.as_button(_("Manage addresses"))
        # elems.append(E.p(btn, align="right"))
        elems.append(E.p(btn))
        return elems
    

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
    messages = dict(
        no_address=_("Owner with address, but no address record."),
        unique_not_primary=_("Unique address is not marked primary."),
        no_primary=_("Multiple addresses, but none is primary."),
        multiple_primary=_("Multiple primary addresses."),
        primary_differs=_("Primary address differs from owner address ({0})."),
    )
    
    def get_plausibility_problems(self, obj, fix=False):
        Address = rt.modules.addresses.Address
        qs = Address.objects.filter(partner=obj)
        num = qs.count()
        if num == 0:
            kw = dict()
            for fldname in Address.ADDRESS_FIELDS:
                v = getattr(obj, fldname)
                if v:
                    kw[fldname] = v
            if kw:
                yield (True, self.messages['no_address'])
                if fix:
                    kw.update(partner=obj, primary=True)
                    kw.update(address_type=AddressTypes.official)
                    addr = Address(**kw)
                    addr.full_clean()
                    addr.save()
            return
    
        def getdiffs(obj, addr):
            diffs = {}
            for k in Address.ADDRESS_FIELDS:
                my = getattr(addr, k)
                other = getattr(obj, k)
                if my != other:
                    diffs[k] = (my, other)
            return diffs

        if num == 1:
            addr = qs[0]
            # check whether it is the same address than the one
            # specified on AddressOwner
            diffs = getdiffs(obj, addr)
            if not diffs:
                if not addr.primary:
                    yield (True, self.messages['unique_not_primary'])
                    if fix:
                        addr.primary = True
                        addr.full_clean()
                        addr.save()
                return
        else:
            addr = None
            qs = qs.filter(primary=True)
            num = qs.count()
            if num == 0:
                yield (False, self.messages['no_primary'])
            elif num == 1:
                addr = qs[0]
                diffs = getdiffs(obj, addr)
            else:
                yield (False, self.messages['multiple_primary'])
        if addr and diffs:
            diffstext = [
                _("{0}:{1}->{2}").format(k, *v) for k, v in list(diffs.items())]
            msg = self.messages['primary_differs'].format(', '.join(diffstext))
            yield (False, msg)

AddressOwnerChecker.activate()
