# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines the classes `dd.AbstractTable` and
:class:`dd.VirtualTable`.

"""

import logging
logger = logging.getLogger(__name__)

import os
import yaml
import json

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
# from django.core.exceptions import PermissionDenied

from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _

from lino.core import constants
from lino.core import actors
from lino.core import actions
from lino.core import fields
from lino.core import signals

from lino.core.dbutils import obj2str

from lino.core.requests import ActionRequest

from lino.ui import base

from lino.utils import jsgen

from lino.utils.xmlgen import html as xghtml
from lino.utils.xmlgen.html import E
# from lino.utils.appy_pod import PrintTableAction, PortraitPrintTableAction


class InvalidRequest(Exception):
    pass

from lino.utils.xmlgen.html import RstTable


if False:  # 20130710

    from lino.utils.config import Configured

    class GridConfig(Configured):

        def __init__(self, report, data, *args, **kw):
            self.report = report
            self.data = data
            self.label_en = data.get('label')
            self.data.update(label=_(self.label_en))
            super(GridConfig, self).__init__(*args, **kw)
            must_save = self.validate()
            if must_save:
                msg = self.save_config()
                #~ msg = self.save_grid_config()
                logger.debug(msg)

        def validate(self):
            """
            Removes unknown columns
            """
            must_save = False
            gc = self.data
            columns = gc['columns']
            col_count = len(columns)
            widths = gc.get('widths', None)
            hiddens = gc.get('hiddens', None)
            if widths is None:
                widths = [None for x in columns]
                gc.update(widths=widths)
            elif col_count != len(widths):
                raise Exception("%d columns, but %d widths" %
                                (col_count, len(widths)))
            if hiddens is None:
                hiddens = [False for x in columns]
                gc.update(hiddens=hiddens)
            elif col_count != len(hiddens):
                raise Exception("%d columns, but %d hiddens" %
                                (col_count, len(hiddens)))

            valid_columns = []
            valid_widths = []
            valid_hiddens = []
            for i, colname in enumerate(gc['columns']):
                f = self.report.get_data_elem(colname)
                if f is None:
                    logger.debug(
                        "Removed unknown column %d (%r). Must save.",
                        i, colname)
                    must_save = True
                else:
                    valid_columns.append(colname)
                    valid_widths.append(widths[i])
                    valid_hiddens.append(hiddens[i])
            gc.update(widths=valid_widths)
            gc.update(hiddens=valid_hiddens)
            gc.update(columns=valid_columns)
            return must_save

        def unused_write_content(self, f):
            self.data.update(label=self.label_en)
            f.write(yaml.dump(self.data))
            self.data.update(label=_(self.label_en))

        def write_content(self, f):
            f.write(yaml.dump(self.data))


WARNINGS_LOGGED = dict()


def column_header(col):
        #~ if col.label:
            #~ return join_elems(col.label.split('\n'),sep=E.br)
        #~ return [unicode(col.name)]
    return unicode(col.label or col.name)


class TableRequest(ActionRequest):
    """Represents an :class:`rt.ActionRequest` on a :class:`table
    <dd.AbstractTable>`.

    """

    master_instance = None
    master = None

    #~ instance = None
    extra = None
    title = None
    #~ layout = None
    filter = None
    known_values = None

    limit = None
    offset = None
    #~ create_rows = None

    _data_iterator = None
    _sliced_data_iterator = None

    def execute(self):

        try:
            self._data_iterator = self.get_data_iterator()
        except Warning as e:
            #~ logger.info("20130809 Warning %s",e)
            self.no_data_text = unicode(e)
            self._data_iterator = []
        except Exception as e:
            # Report this exception. But since such errors may occur
            # rather often and since exception loggers usually send an
            # email to the local system admin, make sure to log an
            # exception only once.
            self.no_data_text = unicode(e)
            w = WARNINGS_LOGGED.get(str(e))
            if w is None:
                WARNINGS_LOGGED[str(e)] = True
                logger.exception(e)
            self._data_iterator = []

        self._sliced_data_iterator = self._data_iterator
        if False:  # self.actor.start_at_bottom:
            if self.offset is not None:
                assert self.limit is not None
                num = self.get_total_count()
                max_pages = int(num / self.limit)
                page = self.offset / self.limit
                page = max_pages - page
                offset = self.limit * page
                # offset = max_offset - self.offset
                self._sliced_data_iterator = self._sliced_data_iterator[
                    offset:]
                self._sliced_data_iterator = self._sliced_data_iterator[
                    :self.limit]
        else:
            if self.offset is not None:
                offset = self.offset
                if offset == -1:
                    assert self.limit is not None
                    num = self.get_total_count()
                    page_num = int(num / self.limit)
                    offset = self.limit * page_num
                self._sliced_data_iterator = self._sliced_data_iterator[
                    offset:]
            if self.limit is not None:
                self._sliced_data_iterator = self._sliced_data_iterator[
                    :self.limit]

    def must_execute(self):
        return self._data_iterator is None

    def get_data_iterator_property(self):
        if self._data_iterator is None:
            self.execute()
        return self._data_iterator

    def get_sliced_data_iterator_property(self):
        if self._sliced_data_iterator is None:
            self.execute()
        return self._sliced_data_iterator

    data_iterator = property(get_data_iterator_property)
    sliced_data_iterator = property(get_sliced_data_iterator_property)

    def get_data_iterator(self):
        if self.actor.get_data_rows is not None:
            l = []
            for row in self.actor.get_data_rows(self):
                #~ if len(l) > 300:
                    #~ raise Exception("20120521 More than 300 items in %s" %
                        #~ unicode(rows))
                group = self.actor.group_from_row(row)
                group.process_row(l, row)
            return l
        #~ logger.info("20120914 tables.get_data_iterator %s",self)
        #~ logger.info("20120914 tables.get_data_iterator %s",self.actor)
        return self.actor.get_request_queryset(self)

    def get_total_count(self):
        """
        Calling `len()` on a QuerySet would execute the whole SELECT.
        See `/blog/2012/0124`
        """
        di = self.data_iterator
        if isinstance(di, QuerySet):
            return di.count()
        #~ if di is None:
            #~ raise Exception("data_iterator is None: %s" % self)
        return len(di)

    def __iter__(self):
        return self.data_iterator.__iter__()

    def parse_req(self, request, rqdata, **kw):
        #~ logger.info("20120723 %s.parse_req()",self.actor)
        #~ rh = self.ah
        master = kw.get('master', self.actor.master)
        if master is not None:
            """
            If `master` is `ContentType` or some abstract model, then
            """
            #~ if master is ContentType or master is models.Model:
            if master is ContentType or master._meta.abstract:
                mt = rqdata.get(constants.URL_PARAM_MASTER_TYPE)
                try:
                    master = kw['master'] = ContentType.objects.get(
                        pk=mt).model_class()
                except ContentType.DoesNotExist:
                    pass
                    # master is None

            if not 'master_instance' in kw:
                pk = rqdata.get(constants.URL_PARAM_MASTER_PK, None)
                #~ print '20100406a', self.actor,URL_PARAM_MASTER_PK,"=",pk
                #~ if pk in ('', '-99999'):
                if pk == '':
                    pk = None
                if pk is None:
                    kw['master_instance'] = None
                else:
                    try:
                        kw['master_instance'] = master.objects.get(pk=pk)
                    except ValueError:
                        raise Exception(
                            "Invalid primary key %r for %s",
                            pk, master.__name__)
                    except master.DoesNotExist:
                        # todo: ReportRequest should become a subclass of
                        # Dialog and this exception should call dlg.error()
                        raise Exception(
                            "%s : There's no %s with primary key %r" %
                            (self.actor, master.__name__, pk))
                # ~ print '20100212', self #, kw['master_instance']
        #~ print '20100406b', self.actor,kw

        if settings.SITE.use_filterRow:
            exclude = dict()
            for f in self.ah.store.fields:
                if f.field:
                    filterOption = rqdata.get(
                        'filter[%s_filterOption]' % f.field.name)
                    if filterOption == 'empty':
                        kw[f.field.name + "__isnull"] = True
                    elif filterOption == 'notempty':
                        kw[f.field.name + "__isnull"] = False
                    else:
                        filterValue = rqdata.get('filter[%s]' % f.field.name)
                        if filterValue:
                            if not filterOption:
                                filterOption = 'contains'
                            if filterOption == 'contains':
                                kw[f.field.name + "__icontains"] = filterValue
                            elif filterOption == 'doesnotcontain':
                                exclude[f.field.name +
                                        "__icontains"] = filterValue
                            else:
                                print "unknown filterOption %r" % filterOption
            if len(exclude):
                kw.update(exclude=exclude)

        if settings.SITE.use_gridfilters:
            filter = rqdata.get(constants.URL_PARAM_GRIDFILTER, None)
            if filter is not None:
                filter = json.loads(filter)
                kw['gridfilters'] = [constants.dict2kw(flt) for flt in filter]

        kw = ActionRequest.parse_req(self, request, rqdata, **kw)
        #~ raise Exception("20120121 %s.parse_req(%s)" % (self,kw))

        #~ kw.update(self.report.known_values)
        #~ for fieldname, default in self.report.known_values.items():
            #~ v = request.REQUEST.get(fieldname,None)
            #~ if v is not None:
                #~ kw[fieldname] = v

        quick_search = rqdata.get(constants.URL_PARAM_FILTER, None)
        if quick_search:
            kw.update(quick_search=quick_search)

        sort = rqdata.get(constants.URL_PARAM_SORT, None)
        if sort:
            #~ self.sort_column = sort
            sort_dir = rqdata.get(constants.URL_PARAM_SORTDIR, 'ASC')
            if sort_dir == 'DESC':
                sort = '-' + sort
                #~ self.sort_direction = 'DESC'
            kw.update(order_by=[sort])

        offset = rqdata.get(constants.URL_PARAM_START, None)
        if offset:
            kw.update(offset=int(offset))
        #~ limit = rqdata.get(constants.URL_PARAM_LIMIT,None)
        limit = rqdata.get(constants.URL_PARAM_LIMIT, self.actor.preview_limit)
        if limit:
            kw.update(limit=int(limit))

        return self.actor.parse_req(request, rqdata, **kw)

    def setup(self,
              quick_search=None,
              order_by=None,
              offset=None, limit=None,
              master=None,
              title=None,
              master_instance=None,
              master_id=None,
              #~ layout=None,
              filter=None,
              #~ create_rows=None,
              gridfilters=None,
              exclude=None,
              extra=None,
              **kw):

        #~ if self.actor.__name__ == 'PrintExpensesByBudget':
            #~ assert master_instance is not None

        self.quick_search = quick_search
        self.order_by = order_by

        #~ logger.info("20120519 %s.setup()",self)
        self.filter = filter
        self.gridfilters = gridfilters
        self.exclude = exclude or self.actor.exclude
        self.extra = extra

        if master is None:
            master = self.actor.master
            # master might still be None
        self.master = master

        if title is not None:
            self.title = title

        if master_id is not None:
            assert master_instance is None
            master_instance = self.master.objects.get(pk=master_id)

        #~ if master is not None:
            #~ if not isinstance(master_instance,master):
                #~ raise Exception("%r is not a %r" % (master_instance,master))

        self.master_instance = master_instance

        #~ AbstractTableRequest.setup(self,**kw)

        """
        Table.page_length is not a default value for ReportRequest.limit
        For example CSVReportRequest wants all rows.
        """
        self.page_length = self.actor.page_length

        #~ logger.info("20120121 %s.setup() done",self)

        #~ if self.actor.__name__ == 'PrintExpensesByBudget':
            #~ print '20130327 1 tables.py', kw.get('master_instance')

        ActionRequest.setup(self, **kw)

        #~ if self.actor.__name__ == 'PrintExpensesByBudget':
            #~ print '20130327 2 tables.py', self, self.master_instance

        # 20120519 : outbox.MyOutbox had no phantom record when called
        # from menu.  When called by permalink it had. Because
        # get_create_kw was called before Actor.setup_request() which
        # sets the master_instance.

        self.actor.setup_request(self)

        self.create_kw = self.actor.get_create_kw(self)

        if offset is not None:
            self.offset = offset

        if limit is not None:
            self.limit = limit

    def table2xhtml(self, header_level=None, **kw):
        t = xghtml.Table()
        self.dump2html(t, self.sliced_data_iterator, **kw)
        e = t.as_element()
        if header_level is not None:
            # return E.div(E.h2(self.get_title()), e)
            return E.div(E.h2(self.actor.label), e)
        return e

    #~ def table2xhtml(self):
        #~ return settings.SITE.ui.table2xhtml(self)

    def dump2html(ar, tble, data_iterator, column_names=None):
        tble.attrib.update(cellspacing="3px", bgcolor="#ffffff", width="100%")

        grid = ar.ah.list_layout.main
        columns = grid.columns
        fields, headers, cellwidths = ar.get_field_info(column_names)
        columns = fields
        #~ print 20130330, cellwidths

        # ~ cellattrs = dict(align="center",valign="middle",bgcolor="#eeeeee")
        cellattrs = dict(align="left", valign="top", bgcolor="#eeeeee")
        # ~ cellattrs = dict(align="left",valign="top",bgcolor="#d0def0")
        #~ cellattrs = dict()

        headers = [
            x for x in grid.headers2html(ar, columns, headers, **cellattrs)]
        sums = [fld.zero for fld in columns]
        #~ hr = tble.add_header_row(*headers,**cellattrs)
        if cellwidths:
            for i, td in enumerate(headers):
                td.attrib.update(width=str(cellwidths[i]))
        tble.head.append(xghtml.E.tr(*headers))
        #~ print 20120623, ar.actor
        recno = 0
        for obj in data_iterator:
            cells = ar.row2html(recno, columns, obj, sums, **cellattrs)
            if cells is not None:
                recno += 1
                #~ ar.actor.apply_row_format(tr,recno)
                tble.body.append(xghtml.E.tr(*cells))

        if recno == 0:
            tble.clear()
            tble.body.append(ar.no_data_text)

        if not ar.actor.hide_sums:
            has_sum = False
            for i in sums:
                if i:
                    has_sum = True
                    break
            if has_sum:
                cells = ar.sums2html(columns, sums, **cellattrs)
                tble.body.append(xghtml.E.tr(*cells))

    def get_field_info(ar, column_names=None):
        u = ar.get_user()
        if u is not None:
            jsgen.set_for_user_profile(u.profile)

        if ar.request is None:
            columns = None
        else:
            columns = [
                str(x) for x in ar.request.REQUEST.getlist(
                    constants.URL_PARAM_COLUMNS)]
        if columns:
            all_widths = ar.request.REQUEST.getlist(
                constants.URL_PARAM_WIDTHS)
            hiddens = [
                (x == 'true') for x in ar.request.REQUEST.getlist(
                    constants.URL_PARAM_HIDDENS)]
            fields = []
            widths = []
            ah = ar.actor.get_handle()
            for i, cn in enumerate(columns):
                col = None
                for e in ah.list_layout.main.columns:
                    if e.name == cn:
                        col = e
                        break
                if col is None:
                    raise Exception("No column named %r in %s" %
                                    (cn, ar.ah.list_layout.main.columns))
                if not hiddens[i]:
                    fields.append(col)
                    widths.append(int(all_widths[i]))
        else:
            if column_names:
                from lino.core import layouts
                ll = layouts.ListLayout(column_names, datasource=ar.actor)
                lh = ll.get_layout_handle(settings.SITE.ui)
                columns = lh.main.columns
                columns = [e for e in columns if not e.hidden]
            else:
                ah = ar.actor.get_request_handle(ar)
                columns = ah.list_layout.main.columns

            # render them so that babelfields in hidden_languages get hidden:
            for e in columns:
                e.value = e.ext_options()
            #
            columns = [e for e in columns if not e.value.get('hidden', False)]

            columns = [e for e in columns if not e.hidden]

            widths = ["%d" % (col.width or col.preferred_width)
                      for col in columns]
            #~ 20130415 widths = ["%d%%" % (col.width or col.preferred_width) for col in columns]
            #~ fields = [col.field._lino_atomizer for col in columns]
            fields = columns

        headers = [column_header(col) for col in fields]

        oh = ar.actor.override_column_headers(ar)
        if oh:
            for i, e in enumerate(columns):
                header = oh.get(e.name, None)
                if header is not None:
                    headers[i] = header
            #~ print 20120507, oh, headers

        return fields, headers, widths

    def row2html(self, recno, columns, row, sums, **cellattrs):
        #~ logger.info("20130123 row2html %s",fields)
        #~ for i,fld in enumerate(self.list_fields):
        has_numeric_value = False
        cells = []
        for i, col in enumerate(columns):
            #~ if fld.name == 'person__gsm':
            #~ logger.info("20120406 Store.row2list %s -> %s", fld, fld.field)
            #~ import pdb; pdb.set_trace()
            v = col.field._lino_atomizer.full_value_from_object(row, self)
            if v is None:
                td = E.td(**cellattrs)
            else:
                nv = col.value2num(v)
                if nv != 0:
                    sums[i] += nv
                    #~ try:
                        #~ sums[i] += nv
                    #~ except TypeError as e:
                        #~ raise Exception("Cannot compute %r + %r" % (sums[i],nv))
                    has_numeric_value = True
                td = col.value2html(self, v, **cellattrs)
            col.apply_cell_format(td)
            self.actor.apply_cell_format(self, row, col, recno, td)
            cells.append(td)
        if self.actor.hide_zero_rows and not has_numeric_value:
            return None
        return cells

    def row2text(self, fields, row, sums):
        for i, fld in enumerate(fields):
            if fld.field is not None:
                try:  # was used to find bug 20130422
                    v = fld.field._lino_atomizer.full_value_from_object(
                        row, self)
                    if v is None:
                        yield ''
                    else:
                        sums[i] += fld.value2num(v)
                        # # In case you want the field name in error message:
                        # try:
                        #     sums[i] += fld.value2num(v)
                        # except Exception as e:
                        #     raise e.__class__("%s %s" % (fld.field, e))
                        yield fld.format_value(self, v)
                except Exception as e:
                    yield "%s:\n%s" % (fld.field, e)

    def sums2html(self, columns, sums, **cellattrs):
        #~ return [fld.format_sum(self,sums,i)
          #~ for i,fld in enumerate(fields)]
        return [fld.sum2html(self, sums, i, **cellattrs)
                for i, fld in enumerate(columns)]

        #~ return [fld.sum2html(self.ui,sums[i])
          #~ for i,fld in enumerate(fields)]

    def get_title(self):
        if self.title is not None:
            return self.title
        return self.actor.get_title(self)

    def get_status(self, **kw):
        kw = ActionRequest.get_status(self, **kw)
        bp = kw['base_params']
        if self.quick_search:
            bp[constants.URL_PARAM_FILTER] = self.quick_search

        if self.known_values:
            for k, v in self.known_values.items():
                if self.actor.known_values.get(k, None) != v:
                    bp[k] = v
        if self.master_instance is not None:
            if self.master is None:
                bp[constants.URL_PARAM_MASTER_PK] = self.master_instance
            else:
                bp[constants.URL_PARAM_MASTER_PK] = self.master_instance.pk
                # if ContentType._meta.installed fails since 20141205
                if settings.SITE.is_installed('contenttypes') \
                   and isinstance(self.master_instance, models.Model):
                    mt = ContentType.objects.get_for_model(
                        self.master_instance.__class__).pk
                    bp[constants.URL_PARAM_MASTER_TYPE] = mt
                else:
                    logger.warning("20141205 %s %s",
                                   self.master_instance,
                                   ContentType)
        return kw

    def __repr__(self):
        #~ kw = dict(actor=str(self.actor))
        kw = dict()
        if self.master_instance is not None:
            #~ kw.update(master_instance=self.master_instance.pk)
            kw.update(master_instance=obj2str(self.master_instance))
        if self.filter is not None:
            kw.update(filter=repr(self.filter))
        if self.known_values:
            kw.update(known_values=self.known_values)
        u = self.get_user()
        if u is not None:
            kw.update(user=u.username)
        #~ return self.__class__.__name__ + '(%s)' % kw
        #~ return self.__class__.__name__ + ' '+str(self.bound_action)+'(%s)' % kw
        return "<%s %s(%s)>" % (self.__class__.__name__, self.bound_action.full_name(), kw)


class TableHandle(base.Handle):

    _layouts = None

    def __init__(self, actor):
        self.actor = actor
        base.Handle.__init__(self)
        #~ super(TableHandle,self).__init__()

    def __str__(self):
        #~ return str(self.ui.__class__)+str(self.actor) + 'Handle'
        return str(self.actor) + 'Handle'

    def setup_layouts(self):
        if self._layouts is not None:
            return
        self._layouts = [self.list_layout]

    def get_actor_url(self, *args, **kw):
        return settings.SITE.ui.get_actor_url(self.actor, *args, **kw)

    def submit_elems(self):
        return []

    def get_list_layout(self):
        self.setup_layouts()
        return self._layouts[0]

    def get_columns(self):
        lh = self.get_list_layout()
        #~ print 20110315, layout._main.columns
        return lh.main.columns

    def get_slaves(self):
        #~ return [ sl.get_handle(self.ui) for sl in self.actor._slaves ]
        return [sl.get_handle(settings.SITE.ui) for sl in self.actor._slaves]


class Group(object):

    def __init__(self):
        self.sums = []

    def process_row(self, collector, row):
        collector.append(row)

    #~ def add_to_table(self,table):
        #~ self.table = table
        #~ for col in table.computed_columns.values():


class AbstractTable(actors.Actor):

    """An AbstractTable is the definition of a tabular data view,
    usually displayed in a Grid (but it's up to the user
    interface to decide how to implement this).

    Base class for :class:`Table <lino.core.dbtables.Table<` and
    :class:`VirtualTable <lino.core.tables.VirtualTable>`.

    """

    _handle_class = TableHandle

    hide_zero_rows = False

    column_names = '*'

    start_at_bottom = False

    group_by = None
    """
    A list of field names that define the groups of rows in this table.
    Each group can have her own header and/or total lines.
    """

    custom_groups = []
    """
    Used internally to store :class:`groups <Group>` defined by this Table.
    """

    get_data_rows = None
    preview_limit = settings.SITE.preview_limit
    variable_row_height = False
    auto_fit_column_widths = False
    active_fields = frozenset()
    hidden_columns = frozenset()

    form_class = None
    help_url = None

    page_length = 20
    """Number of rows to display per page.  Used to control the height of
    a combobox of a ForeignKey pointing to this model

    """

    cell_edit = True

    show_detail_navigator = False
    """
    Whether a Detail view on a row of this table should have a navigator.
    """

    default_group = Group()

    #~ default_action = GridEdit
    default_layout = 0

    typo_check = True
    """
    True means that Lino shoud issue a warning if a subclass
    defines any attribute that did not exist in the base class.
    Usually such a warning means that there is something wrong.
    """

    slave_grid_format = 'grid'

    grid_configs = []
    """
    Will be filled during :meth:`lino.core.table.Table.do_setup`.
    """

    order_by = None

    filter = None
    exclude = None

    extra = None
    """
    Examples::
    
      extra = dict(select=dict(lower_name='lower(name)'))
      # (or if you prefer:) 
      # extra = {'select':{'lower_name':'lower(name)'},'order_by'=['lower_name']}
    
    List of SQL functions and which RDBMS supports them:
    http://en.wikibooks.org/wiki/SQL_Dialects_Reference/Functions_and_expressions/String_functions
    
    """

    def __init__(self, *args, **kw):
        raise NotImplementedError("20120104")

    @classmethod
    def spawn(cls, suffix, **kw):
        kw['app_label'] = cls.app_label
        return type(cls.__name__ + str(suffix), (cls,), kw)

    @classmethod
    def parse_req(self, request, rqdata, **kw):
        return kw

    @classmethod
    def get_row_by_pk(self, ar, pk):
        """
        `dbtables.Table` overrides this.
        """
        try:
            return ar.data_iterator[int(pk)-1]
        except (ValueError, IndexError):
            return None

    @classmethod
    def get_default_action(cls):
        #~ return actions.BoundAction(cls,cls.grid)
        #~ return 'grid'
        return actions.GridEdit()

    @classmethod
    def get_actor_editable(self):
        if self._editable is None:
            return (self.get_data_rows is None)
        return self._editable

    @classmethod
    def setup_columns(self):
        pass

    @classmethod
    def get_column_names(self, ar):
        return self.column_names

    @classmethod
    def group_from_row(self, row):
        return self.default_group

    @classmethod
    def wildcard_data_elems(self):
        for cc in self.virtual_fields.values():
            yield cc
        #~ return []

    @classmethod
    def save_grid_config(self, index, data):
        raise Exception("20130710")
        if len(self.grid_configs) == 0:
            gc = GridConfig(self, data, '%s.gc' % self)
            self.grid_configs.append(gc)
        else:
            gc = self.grid_configs[index]
        gc.data = data
        gc.validate()
        #~ self.grid_configs[index] = gc
        return gc.save_config()
        #~ filename = self.get_grid_config_file(gc)
        #~ f = open(filename,'w')
        # ~ f.write("# Generated file. Delete it to restore default configuration.\n")
        #~ d = dict(grid_configs=self.grid_configs)
        #~ f.write(yaml.dump(d))
        #~ f.close()
        #~ return "Grid Config has been saved to %s" % filename

    @classmethod
    def get_create_kw(self, ar, **kw):
        """Deprecated.  This additional wrapper was used by
        `lino.modlib.links` which anyway never worked.  We will soon
        throw it away and call get_filter_kw directly instead.

        """
        return self.get_filter_kw(ar, **kw)

    @classmethod
    def get_filter_kw(self, ar, **kw):
        master_instance = ar.master_instance
        if self.master is None:
            pass
            # master_instance may be e.g. a lino.core.actions.EmptyTableRow
            # UsersWithClients as "slave" of the "table" Home
        elif self.master is models.Model:
            pass
        elif isinstance(self.master_field, generic.GenericForeignKey):
        #~ elif self.master is ContentType:
            #~ print 20110415
            if master_instance is None:
                """
                20120222 : here was only `pass`, and the two other lines
                were uncommented. don't remember why I commented them out.
                But it caused all tasks to appear in UploadsByController of
                an insert window for uploads.
                """
                #~ pass
                kw[self.master_field.ct_field] = None
                kw[self.master_field.fk_field] = None
            else:
                ct = ContentType.objects.get_for_model(
                    master_instance.__class__)
                kw[self.master_field.ct_field] = ct
                kw[self.master_field.fk_field] = master_instance.pk
        elif self.master_field is not None:
            if master_instance is None:
                if not self.master_field.null:
                    #~ logger.info('20120519 %s.get_filter_kw()--> None',self)
                    return  # cannot add rows to this table
            else:
                master_instance = master_instance.get_typed_instance(
                    self.master)
                if not isinstance(master_instance, self.master):
                    # e.g. a ByUser table descendant called by AnonymousUser
                    msg = "%r is not a %s (%s.master_key = '%s')" % (
                        master_instance.__class__,
                        self.master, self,
                        self.master_key)
                    logger.warning(msg)
                    # raise Exception(msg)
                    # raise PermissionDenied(msg)
                    # master_instance = None
                    return  # cannot add rows to this table
            kw[self.master_field.name] = master_instance

        return kw

    #~ @classmethod
    #~ def request(cls,ui=None,request=None,action=None,**kw):
        #~ self = cls
        #~ if action is None:
            #~ action = self.default_action
        #~ return TableRequest(ui,self,request,action,**kw)

    @classmethod
    def request(self, master_instance=None, **kw):
        kw.update(actor=self)
        if master_instance is not None:
            kw.update(master_instance=master_instance)
        return TableRequest(**kw)

    @classmethod
    def run_action_from_console(self, pk=None, an=None):
        """
        Not yet stable. Used by print_tx25.py.
        To be combined with the `show` management command.
        """
        settings.SITE.startup()
        #~ settings.SITE.ui
        if pk is not None:
            #~ elem = self.get_row_by_pk(pk)
            #~ elem = self.model.objects.get(pk=pk)
            if an is None:
                an = self.default_elem_action_name
        elif an is None:
            an = self.default_list_action_name
        ba = self.get_action_by_name(an)
        #~ print ba
        if pk is None:
            ar = self.request(action=ba)
        else:
            ar = self.request(action=ba, selected_pks=[pk])

        ba.action.run_from_ui(ar)
        kw = ar.response
        msg = kw.get('message')
        if msg:
            print msg
        url = kw.get('open_url') or kw.get('open_davlink_url')
        if url:
            os.startfile(url)

    @classmethod
    def to_rst(cls, ar, column_names=None, header_level=None, **kwargs):
        "Better name would be table2rst (analog to table2xhtml())"
        fields, headers, widths = ar.get_field_info(column_names)

        sums = [fld.zero for fld in fields]
        rows = []
        recno = 0
        for row in ar.sliced_data_iterator:
            recno += 1
            rows.append([x for x in ar.row2text(fields, row, sums)])

        if not cls.hide_sums:
            has_sum = False
            for i in sums:
                if i:
                    #~ print '20120914 zero?', repr(i)
                    has_sum = True
                    break
            if has_sum:
                rows.append([x for x in ar.sums2html(fields, sums)])

        t = RstTable(headers, **kwargs)
        s = t.to_rst(rows)
        if header_level is not None:
            s = E.tostring(E.h2(ar.get_title())) + s
        return s


class VirtualTable(AbstractTable):
    """
    An :class:`AbstractTable` that works on an volatile (non
    persistent) list of rows.

    By nature it cannot have database fields, only virtual fields.

    Subclasses must define a :meth:`get_data_rows` method.

    """
    pass


class VentilatingTable(AbstractTable):

    ventilated_column_suffix = ':5'

    @fields.virtualfield(models.CharField(_("Description"), max_length=30))
    def description(self, obj, ar):
        return unicode(obj)

    @classmethod
    def setup_columns(self):
        self.column_names = 'description '
        for i, vf in enumerate(self.get_ventilated_columns()):
            self.add_virtual_field('vc' + str(i), vf)
            self.column_names += ' ' + vf.name + self.ventilated_column_suffix
        #~ logger.info("20131114 setup_columns() --> %s",self.column_names)

    @classmethod
    def get_ventilated_columns(self):
        return []


from lino.core.signals import database_ready


@signals.receiver(database_ready)
def setup_ventilated_columns(sender, **kw):
    if actors.actors_list is not None:
        for a in actors.actors_list:
            if issubclass(a, AbstractTable):
                a.setup_columns()
    settings.SITE.resolve_virtual_fields()
