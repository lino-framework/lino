# -*- coding: UTF-8 -*-
# Copyright 2009-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines the `TableRequest` class.

"""
from __future__ import division
from __future__ import print_function
# from future import standard_library
# standard_library.install_aliases()
from builtins import str
from past.utils import old_div
import six

import logging
logger = logging.getLogger(__name__)

from types import GeneratorType
import sys
from io import StringIO
import json

from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation

from lino.core.utils import obj2str
from lino.core.utils import format_request
from lino.core.store import get_atomizer
from lino.core import constants
from etgen import html as xghtml
from etgen.html import E
from lino.utils import jsgen
from lino.core.utils import getrqdata
from .fields import RemoteField, FakeField, TableRow

from .requests import ActionRequest

WARNINGS_LOGGED = dict()


def column_header(col):
        #~ if col.label:
            #~ return join_elems(col.label.split('\n'),sep=E.br)
        #~ return [unicode(col.name)]
    label = col.get_label()
    if label is None:
        return col.name
    return six.text_type(label)


class TableRequest(ActionRequest):
    """A specialized :class:`ActionRequest
    <lino.core.requests.ActionRequest>` whose actor is a :class:`table
    <lino.core.tables.AbstractTable>`.

    """

    master = None

    extra = None
    title = None
    filter = None
    # known_values = None

    limit = None
    offset = None

    _data_iterator = None
    _sliced_data_iterator = None

    def execute(self):
        """This will actually call the :meth:`get_data_iterator` and run the
        database query.

        Automatically called when either :attr:`data_iterator`
        or :attr:`sliced_data_iterator` is accesed.

        """
        # print("20181121 execute", self.actor)
        try:
            self._data_iterator = self.get_data_iterator()
            if self._data_iterator is None:
                raise Exception("No data iterator for {}".format(self))
        except Warning as e:
            #~ logger.info("20130809 Warning %s",e)
            self.no_data_text = six.text_type(e)
            self._data_iterator = []
        except Exception as e:
            if not settings.SITE.catch_layout_exceptions:
                raise
            # Report this exception. But since such errors may occur
            # rather often and since exception loggers usually send an
            # email to the local system admin, make sure to log each
            # exception only once.
            self.no_data_text = six.text_type(e)
            w = WARNINGS_LOGGED.get(six.text_type(e))
            if w is None:
                WARNINGS_LOGGED[six.text_type(e)] = True
                raise
                # logger.exception(e)
            self._data_iterator = []

        if isinstance(self._data_iterator, GeneratorType):
            # print 20150718, self._data_iterator
            self._data_iterator = tuple(self._data_iterator)
        self._sliced_data_iterator = self._data_iterator
        if False:  # self.actor.start_at_bottom:
            if self.offset is not None:
                assert self.limit is not None
                num = self.get_total_count()
                max_pages = int(old_div(num, self.limit))
                page = old_div(self.offset, self.limit)
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
                    page_num = int(old_div(num, self.limit))
                    offset = self.limit * page_num
                self._sliced_data_iterator = self._sliced_data_iterator[
                    offset:]
            if self.limit is not None:
                self._sliced_data_iterator = self._sliced_data_iterator[
                    :self.limit]
        # logger.info("20171116 executed : %s", self._sliced_data_iterator)

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
        self.actor.check_params(self.param_values)
        if self.actor.get_data_rows is not None:
            l = []
            for row in self.actor.get_data_rows(self):
                group = self.actor.group_from_row(row)
                group.process_row(l, row)
            return l
        #~ logger.info("20120914 tables.get_data_iterator %s",self)
        #~ logger.info("20120914 tables.get_data_iterator %s",self.actor)
        # print("20181121 get_data_iterator", self.actor)
        return self.actor.get_request_queryset(self)

    def get_total_count(self):
        """
        Calling `len()` on a QuerySet would execute the whole SELECT.
        See `/blog/2012/0124`
        """
        di = self.data_iterator
        if isinstance(di, QuerySet):
            return di.count()
            # try:
            #     return di.count()
            # except Exception as e:
            #     raise e.__class__("{} : {}".format(self, e))
        #~ if di is None:
            #~ raise Exception("data_iterator is None: %s" % self)
        if False:
            return len(di)
        else:
            try:
                return len(di)
            except TypeError:
                raise TypeError("{0} has no length".format(di))

    def __iter__(self):
        return self.data_iterator.__iter__()

    def __getitem__(self, i):
        return self.data_iterator.__getitem__(i)

    def parse_req(self, request, rqdata, **kw):
        """Parse the incoming HttpRequest and translate it into keyword
        arguments to be used by :meth:`setup`.

        The `mt` url param is parsed only when needed. Usually it is
        not needed because the `master_class` is constant and known
        per actor. But there are exceptions:

        - `master` is `ContentType`

        - `master` is some abstract model

        - `master` is not a subclass of Model, e.g.
          :class:`lino_xl.lib.polls.models.AnswersByResponse`, a
          virtual table which defines :meth:`get_row_by_pk
          <lino.core.actors.Actor.get_row_by_pk>`.

        """
        # logger.info("20120723 %s.parse_req() %s", self.actor, rqdata)
        #~ rh = self.ah
        master = kw.get('master', self.actor.master)
        if master is not None:

            if not isinstance(master, type):
                raise Exception("20150216 not a type: %r" % master)
            if settings.SITE.is_installed('contenttypes'):
                from django.contrib.contenttypes.models import ContentType
                if issubclass(master, models.Model) and (
                        master is ContentType or master._meta.abstract):
                    mt = rqdata.get(constants.URL_PARAM_MASTER_TYPE)
                    try:
                        master = kw['master'] = ContentType.objects.get(
                            pk=mt).model_class()
                    except ContentType.DoesNotExist:
                        pass
                        # master is None

            if 'master_instance' not in kw:
                pk = rqdata.get(constants.URL_PARAM_MASTER_PK, None)
                #~ print '20100406a', self.actor,URL_PARAM_MASTER_PK,"=",pk
                #~ if pk in ('', '-99999'):
                if pk == '':
                    pk = None
                if pk is None:
                    kw['master_instance'] = None
                else:
                    mi = self.actor.get_master_instance(self, master, pk)
                    if mi is None:
                        raise ObjectDoesNotExist(
                            "Invalid master key {0} for {1}".format(
                                pk, self.actor))
                    kw['master_instance'] = mi

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
                                print("unknown filterOption %r" % filterOption)
            if len(exclude):
                kw.update(exclude=exclude)

        if settings.SITE.use_gridfilters:
            filter = rqdata.get(constants.URL_PARAM_GRIDFILTER, None)
            if filter is not None:
                filter = json.loads(filter)
                kw['gridfilters'] = [constants.dict2kw(flt) for flt in filter]

        kw = ActionRequest.parse_req(self, request, rqdata, **kw)

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
            sortfld = self.actor.get_data_elem(sort)
            if isinstance(sortfld, FakeField):
                sort = sortfld.sortable_by
                # sort might be None when user asked to sort a virtual
                # field without sortable_by.
            else:
                sort = [sort]
            if sort is not None:
                def si(k):
                   if k[0] == '-':
                       return k[1:]
                   else:
                       return '-' + k 
                sort_dir = rqdata.get(constants.URL_PARAM_SORTDIR, 'ASC')
                if sort_dir == 'DESC':
                    sort = [si(k) for k in sort]
                    # sort = ['-' + k for k in sort]
                # print("20171123", sort)
                kw.update(order_by=sort)

        try:
            offset = rqdata.get(constants.URL_PARAM_START, None)
            if offset:
                kw.update(offset=int(offset))
            limit = rqdata.get(
                constants.URL_PARAM_LIMIT, self.actor.preview_limit)
            if limit:
                kw.update(limit=int(limit))
        except ValueError:
            # Example: invalid literal for int() with base 10:
            # 'fdpkvcnrfdybhur'
            raise SuspiciousOperation("Invalid value for limit or offset")

        kw = self.actor.parse_req(request, rqdata, **kw)
        # print("20171123 %s.parse_req() --> %s" % (self, kw))
        return kw

    def setup(self,
              quick_search=None,
              order_by=None,
              offset=None, limit=None,
              master=None,
              title=None,
              master_id=None,
              filter=None,
              gridfilters=None,
              exclude=None,
              extra=None,
              **kw):

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
            raise Exception("20150218 deprecated?")
            # assert master_instance is None
            # master_instance = self.master.objects.get(pk=master_id)

        self.page_length = self.actor.page_length

        #~ logger.info("20120121 %s.setup() done",self)

        ActionRequest.setup(self, **kw)

        self.actor.setup_request(self)

        if isinstance(self.actor.master_field, RemoteField):
            # cannot insert rows in a slave table with a remote master
            # field
            self.create_kw = None
        else:
            self.create_kw = self.actor.get_filter_kw(self)

        if offset is not None:
            self.offset = offset

        if limit is not None:
            self.limit = limit
            

    def to_rst(self, *args, **kw):
        """Returns a string representing this table request in
        reStructuredText markup.

        """
        stdout = sys.stdout
        sys.stdout = StringIO()
        self.table2rst(*args, **kw)
        rv = sys.stdout.getvalue()
        sys.stdout = stdout
        return rv

    def table2rst(self, *args, **kwargs):
        """
        Print a reStructuredText representation of this table request to
        stdout.
        """
        settings.SITE.kernel.text_renderer.show_table(self, *args, **kwargs)

    def table2xhtml(self, **kwargs):
        """
        Return an HTML representation of this table request.
        """
        t = xghtml.Table()
        self.dump2html(t, self.sliced_data_iterator, **kwargs)
        e = t.as_element()
        # print "20150822 table2xhtml", tostring(e)
        # if header_level is not None:
        #     return E.div(E.h2(str(self.actor.label)), e)
        return e

    def dump2html(self, tble, data_iterator, column_names=None,
                  header_links=False, hide_sums=None):
        """
        Render this table into an existing :class:`etgen.html.Table`
        instance.  This is central method is used by all Lino
        renderers.

        Arguments:

        `tble` An instance of :class:`etgen.html.Table`.

        `data_iterator` the iterable provider of table rows.  This can
        be a queryset or a list.

        `column_names` is an optional string with space-separated
        column names.  If this is None, the table's
        :attr:`column_names <lino.core.tables.Table.column_names>` is
        used.

        `header_links` says whether to render column headers clickable
        with a link that sorts the table.

        `hide_sums` : whether to hide sums. If this is not given, use
        the :attr:`hide_sums <lino.core.tables.Table.hide_sums>` of
        the :attr:`actor`.
        """
        ar = self
        tble.attrib.update(self.renderer.tableattrs)
        tble.attrib.setdefault('name', self.bound_action.full_name())

        grid = ar.ah.list_layout.main
        # from lino.core.widgets import GridWidget
        # if not isinstance(grid, GridWidget):
        #     raise Exception("20160529 %r is not a GridElement", grid)
        columns = grid.columns
        fields, headers, cellwidths = ar.get_field_info(column_names)
        columns = fields

        sums = [fld.zero for fld in columns]
        if not self.ah.actor.hide_headers:
            headers = [
                x for x in grid.headers2html(
                    self, columns, headers, header_links,
                    **self.renderer.cellattrs)]
            # if cellwidths and self.renderer.is_interactive:
            if cellwidths:
                totwidth = sum([int(w) for w in cellwidths])
                widths = [str(int(int(w)*100/totwidth))+"%"
                        for w in cellwidths]
                for i, td in enumerate(headers):
                    # td.set('width', six.text_type(cellwidths[i]))
                    td.set('width', widths[i])
            tble.head.append(xghtml.E.tr(*headers))
        #~ print 20120623, ar.actor
        recno = 0
        for obj in data_iterator:
            cells = ar.row2html(
                recno, columns, obj, sums, **self.renderer.cellattrs)
            if cells is not None:
                recno += 1
                tble.body.append(xghtml.E.tr(*cells))

        if recno == 0:
            tble.clear()
            tble.body.append(str(ar.no_data_text))

        if hide_sums is None:
            hide_sums = ar.actor.hide_sums

        if not hide_sums:
            has_sum = False
            for i in sums:
                if i:
                    has_sum = True
                    break
            if has_sum:
                cells = ar.sums2html(columns, sums, **self.renderer.cellattrs)
                tble.body.append(xghtml.E.tr(*cells))

    def get_field_info(ar, column_names=None):
        """
        Return a tuple `(fields, headers, widths)` which expresses which
        columns, headers and widths the user wants for this
        request. If `self` has web request info (:attr:`request` is
        not None), checks for GET parameters cn, cw and ch.  Also
        calls the tables's :meth:`override_column_headers
        <lino.core.actors.Actor.override_column_headers>` method.
        """
        from lino.modlib.users.utils import with_user_profile
        from lino.core.layouts import ColumnsLayout

        def getit():

            if ar.request is None:
                columns = None
            else:
                data = getrqdata(ar.request)
                columns = [
                    six.text_type(x) for x in
                    data.getlist(constants.URL_PARAM_COLUMNS)]
            if columns:
                all_widths = data.getlist(constants.URL_PARAM_WIDTHS)
                hiddens = [(x == 'true') for x in data.getlist(
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
                    ll = ColumnsLayout(column_names, datasource=ar.actor)
                    lh = ll.get_layout_handle(settings.SITE.kernel.default_ui)
                    columns = lh.main.columns
                    columns = [e for e in columns if not e.hidden]
                else:
                    ah = ar.actor.get_request_handle(ar)
                    
                    columns = ah.list_layout.main.columns
                    # print(20160530, ah, columns, ah.list_layout.main)

                # render them so that babelfields in hidden_languages
                # get hidden:
                for e in columns:
                    e.value = e.ext_options()
                    # try:
                    #     e.value = e.ext_options()
                    # except AttributeError as ex:
                    #     raise AttributeError("20160529 %s : %s" % (e, ex))
                #
                columns = [e for e in columns if not
                           e.value.get('hidden', False)]

                columns = [e for e in columns if not e.hidden]

                # if str(ar.actor) == "isip.ExamPolicies":
                    # from lino.modlib.extjs.elems import is_hidden_babel_field
                    # print("20180103", [c.name for c in columns])
                    # print("20180103", [c.field for c in columns])
                    # print("20180103", [c.value['hidden'] for c in columns])
                    # print("20180103", [
                    #     is_hidden_babel_field(c.field) for c in columns])
                    # print("20180103", [
                    #     getattr(c.field, '_babel_language', None)
                    #     for c in columns])
                widths = ["%d" % (col.width or col.preferred_width)
                          for col in columns]
                # print("20180831 {}".format(widths))
                #~ 20130415 widths = ["%d%%" % (col.width or col.preferred_width) for col in columns]
                #~ fields = [col.field._lino_atomizer for col in columns]
                fields = columns

            headers = [column_header(col) for col in fields]

            # if str(ar.actor).endswith("DailyPlanner"):
            #     print("20181022", fields[0].field.verbose_name)

            oh = ar.actor.override_column_headers(ar)
            if oh:
                for i, e in enumerate(columns):
                    header = oh.get(e.name, None)
                    if header is not None:
                        headers[i] = header
                #~ print 20120507, oh, headers

            return fields, headers, widths
    
        u = ar.get_user()
        if u is None:
            return getit()
        else:
            return with_user_profile(u.user_type, getit)

    def row2html(self, recno, columns, row, sums, **cellattrs):
        has_numeric_value = False
        cells = []
        for i, col in enumerate(columns):
            v = col.field._lino_atomizer.full_value_from_object(row, self)
            if v is None:
                td = E.td(**cellattrs)
            else:
                nv = col.value2num(v)
                if nv != 0:
                    sums[i] += nv
                    has_numeric_value = True
                td = col.value2html(self, v, **cellattrs)
            col.apply_cell_format(td)
            self.actor.apply_cell_format(self, row, col, recno, td)
            cells.append(td)
        if self.actor.hide_zero_rows and not has_numeric_value:
            return None
        return cells

    def row2text(self, fields, row, sums):
        """Render the given `row` into a line of text, using the given list of
        `fields` and collecting sums into `sums`.

        """
        # print(20160530, fields)
        for i, fld in enumerate(fields):
            if fld.field is not None:
                sf = get_atomizer(row.__class__, fld.field, fld.field.name)
                # print(20160530, fld.field.name, sf)
                if False:
                    try:
                        getter = sf.full_value_from_object
                        v = getter(row, self)
                    except Exception as e:
                        raise Exception("20150218 %s: %s" % (sf, e))
                        # was used to find bug 20130422:
                        yield "%s:\n%s" % (fld.field, e)
                        continue
                else:
                    getter = sf.full_value_from_object
                    v = getter(row, self)
                    
                if v is None:
                # if not v:
                    yield ''
                else:
                    sums[i] += fld.value2num(v)
                    # # In case you want the field name in error message:
                    # try:
                    #     sums[i] += fld.value2num(v)
                    # except Exception as e:
                    #     raise e.__class__("%s %s" % (fld.field, e))
                    yield fld.format_value(self, v)

    def sums2html(self, columns, sums, **cellattrs):
        sums = {fld.name: sums[i] for i, fld in enumerate(columns)}
        return [fld.sum2html(self, sums, i, **cellattrs)
                for i, fld in enumerate(columns)]

    def get_title(self):
        if self.title is not None:
            return self.title
        if self.master_instance is not None:
            self.master_instance
        return self.actor.get_title(self)

    def get_status(self, **kw):
        """Extends :meth:`lino.core.requests.ActorRequest.get_status`.

        """
        kw = ActionRequest.get_status(self, **kw)
        bp = kw['base_params']
        if self.quick_search:
            bp[constants.URL_PARAM_FILTER] = self.quick_search

        if self.order_by:
            sort = self.order_by[0]
            if sort.startswith('-'):
                sort = sort[1:]
                bp[constants.URL_PARAM_SORTDIR] = 'DESC'
            bp[constants.URL_PARAM_SORT] = sort

        if self.known_values:
            for k, v in self.known_values.items():
                if self.actor.known_values.get(k, None) != v:
                    bp[k] = v
        if self.master_instance is not None:
            if isinstance(self.master_instance, (models.Model, TableRow)):
                bp[constants.URL_PARAM_MASTER_PK] = self.master_instance.pk
                if (isinstance(self.master_instance, models.Model) and
                              settings.SITE.is_installed('contenttypes')):
                    from django.contrib.contenttypes.models import ContentType
                    mt = ContentType.objects.get_for_model(
                        self.master_instance.__class__).pk
                    bp[constants.URL_PARAM_MASTER_TYPE] = mt
                # else:
                #     logger.warning("20141205 %s %s",
                #                    self.master_instance,
                #                    ContentType)
            else:  # if self.master is None:
                bp[constants.URL_PARAM_MASTER_PK] = self.master_instance
            
        return kw

    def __repr__(self):
        kw = dict()
        if self.master_instance is not None:
            kw.update(master_instance=obj2str(self.master_instance))
        if self.filter is not None:
            kw.update(filter=repr(self.filter))
        if self.known_values:
            kw.update(known_values=self.known_values)
        if self.requesting_panel:
            kw.update(requesting_panel=self.requesting_panel)
        u = self.get_user()
        if u is not None:
            kw.update(user=u.username)
        if False:  # self.request:
            kw.update(request=format_request(self.request))
        return "<%s %s(%s)>" % (
            self.__class__.__name__, self.bound_action.full_name(), kw)


