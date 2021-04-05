# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
This defines the :class:`MergeAction` class.

See :doc:`/dev/merge`.

"""

import logging ; logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext

from lino.core import actions
from lino.core import layouts
from lino.core import fields
from lino.core.signals import pre_merge
from lino.core.utils import full_model_name, traverse_ddh_fklist
from lino.core.roles import Expert
from etgen.html import E
from lino.api import rt


class MergeAction(actions.Action):
    label = _("Merge")
    icon_name = 'arrow_join'
    ui5_icon_name = "sap-icon://font-awesome-solid/code-branch"
    # ui5_icon_name = "sap-icon://detail-view"
    sort_index = 31
    show_in_workflow = False
    readonly = False
    required_roles = set([Expert])

    def __init__(self, model, **kw):

        parameters = dict(
            #~ merge_from=models.ForeignKey(model,verbose_name=_("Merge...")),
            merge_to=fields.ForeignKey(
                model, verbose_name=_("into..."), blank=False, null=False),
            reason=models.CharField(_("Reason"), max_length=100)
            #~ notify=models.BooleanField(_("Send notifications"))
        )

        keep_volatiles = []

        # logger.info("20160621 MergeAction for %s", model)
        # logger.info("20160621 MergeAction for %s : _lino_ddh.fklist is %s",
        #             model, model._lino_ddh.fklist)
        for m, fk in traverse_ddh_fklist(model):
            if fk.name in m.allow_cascaded_delete:
                fieldname = full_model_name(m, '_')
                if fieldname not in keep_volatiles:
                    keep_volatiles.append(fieldname)
                    parameters[fieldname] = models.BooleanField(
                        m._meta.verbose_name_plural, default=False)
                # logger.info(
                #     "20160621 %r in %r", fk.name, m.allow_cascaded_delete)

        layout = dict()
        if len(keep_volatiles) == 0:
            width = 50
            main = """
            merge_to
            reason
            """
        else:
            COLCOUNT = 2
            width = 70
            if len(keep_volatiles) > COLCOUNT:
                tpl = ''
                for i, name in enumerate(keep_volatiles):
                    if i % COLCOUNT == 0:
                        tpl += '\n'
                    else:
                        tpl += ' '
                    tpl += name
            else:
                tpl = ' '.join(keep_volatiles)
            main = """
            merge_to
            keep_volatiles
            reason
            """
            layout.update(keep_volatiles=layouts.Panel(
                tpl, label=_("Also reassign volatile related objects")))

        layout.update(window_size=(width, 'auto'))
        kw.update(
            parameters=parameters,
            params_layout=layouts.Panel(main, **layout))

        super(MergeAction, self).__init__(**kw)

    #~ def action_param_defaults(self,ar,obj,**kw):
        #~ kw = super(MergeAction,self).action_param_defaults(ar,obj,**kw)
        #~ kw.update(merge_from=obj)
        #~ return kw

    def run_from_ui(self, ar):
        """
        Implements :meth:`lino.core.actions.Action.run_from_ui`.
        """
        obj = ar.selected_rows[0]

        if ar.action_param_values.merge_to is None:
            raise Warning(_("You must specify a merge target."))

        mp = MergePlan(obj, ar.action_param_values.merge_to,
                       ar.action_param_values)
        msg = mp.build_confirmation_message()

        def ok(ar2):
            logger.info("Gonna execute merge plan %s", mp.logmsg())
            msg = mp.execute(request=ar.request)
            ar2.goto_instance(mp.merge_to)
            ar2.success(msg, alert=True, close_window=True)
            logger.info("%s : %s", ar.get_user(), msg)

        if msg is None:
            raise Exception("20180523")
            return ok(ar)
        ar.confirm(ok, msg)


class MergePlan(object):
    """A volatile object which represents what is going to happen if we
    merge two objects.

    """

    def __init__(self, obj, merge_to, keep_volatiles={}):
        if merge_to == obj:
            raise Warning(_("Cannot merge an instance to itself."))
        self.obj = obj
        self.merge_to = merge_to
        self.keep_volatiles = keep_volatiles

    def analyze(self):
        self.volatiles = []
        self.related = []
        self.generic_related = []
        # logger.info("20160621 ddh.fklist is %s", self.obj._lino_ddh.fklist)
        for m, fk in traverse_ddh_fklist(self.obj.__class__):
            qs = m.objects.filter(**{fk.name: self.obj})
            if fk.name in m.allow_cascaded_delete and \
               not self.keep_volatiles.get(full_model_name(m, '_')):
                self.volatiles.append((fk, qs))
            else:
                self.related.append((fk, qs))
        for gfk, fk, qs in settings.SITE.kernel.get_generic_related(self.obj):
            if not getattr(gfk, 'dont_merge', False):
                self.generic_related.append((gfk, qs))

    def logmsg(self):
        #~ self.analyze()
        lst = []
        lst.append(_("Merge %(origin)s into %(target)s") %
                   dict(origin=self.obj, target=self.merge_to))

        def add(name):
            for f, qs in getattr(self, name):
                if qs.count() > 0:
                    lst.append('- %d %s %s rows using %s : %s' % (
                        qs.count(),
                        name,
                        full_model_name(f.model),
                        f.name,
                        ' '.join([str(o.pk) for o in qs])))
        add('volatiles')
        add('related')
        add('generic_related')
        return '\n'.join(lst)

    def build_confirmation_message(self):
        self.analyze()
        items = []

        def collect_summary(prefix, fk_qs):
            parts = []
            for fld, qs in fk_qs:
                if qs.count() > 0:
                    parts.append(
                        "%d %s" % (
                            qs.count(), str(
                                fld.model._meta.verbose_name_plural)))
            if len(parts) != 0:
                items.append(E.li(', '.join(parts), ' ', E.b(prefix)))

        collect_summary(gettext("will be deleted."), self.volatiles)
        collect_summary(gettext("will get reassigned."),
                        self.related + self.generic_related)
        items.append(E.li(gettext("%s will be deleted") % self.obj))
        msg = gettext("Are you sure you want to merge "
                "%(this)s into %(merge_to)s?") % dict(
                    this=self.obj, merge_to=self.merge_to)
        if len(items) != 0:
            return rt.html_text(E.div(E.p(msg), E.ul(*items)))
        return msg

    def execute(self, **kw):
        self.analyze()  # refresh since there may be changes since summary()
        # give others a chance to object
        #~ pre_merge.send(self.obj,merge_to=self.merge_to)
        kw.update(sender=self)
        pre_merge.send(**kw)
        update_count = 0
        # change FK fields of related objects
        for fk, qs in self.related:
            # if qs.model.__name__ == 'Guest':
            #     print(20160621, fk.name, self.merge_to.pk, self.obj.pk, qs, str(qs.query))
            update_count += qs.update(**{fk.name: self.merge_to})
            #~ for relobj in qs:
                #~ setattr(relobj,fk.name,merge_to)
                #~ relobj.full_clean()
                #~ relobj.save()

        # merge GenericForeignKey relations
        for gfk, qs in self.generic_related:
            update_count += qs.update(**{gfk.fk_field: self.merge_to.pk})
            #~ for i in qs:
                #~ setattr(qs,gfk.fk_field,merge_to.pk)
                # ~ # setattr(qs,gfk.name,merge_to)
                #~ i.full_clean()
                #~ i.save()

        # Build the return message
        msg = _("Merged %(this)s into %(merge_to)s. "
                "Updated %(updated)d related rows.") % dict(
                    this=self.obj, merge_to=self.merge_to,
                    updated=update_count)

        # Delete object from database:
        self.obj.delete()

        # Delete the reference to the deleted object:
        del self.obj
        return msg
