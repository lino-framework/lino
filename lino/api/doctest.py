# -*- coding: UTF-8 -*-
# Copyright 2015-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
A selection of names to be used in tested documents.
"""

import six  # TODO: remove here and then run all doctests

import django
django.setup()
from lino.api.shell import *
from django.utils import translation
from django.utils.encoding import force_text
from django.test import Client
from django.db import connection, reset_queries as reset_sql_queries
import json
from bs4 import BeautifulSoup

from rstgen import table
import rstgen
from rstgen import attrtable
from atelier.utils import unindent, rmu, sixprint

from lino.utils import AttrDict
from lino.utils import i2d
from etgen.html import E, tostring, to_rst
from lino.utils.diag import analyzer
from lino.utils import diag
from lino.utils.sql import sql_summary
from lino.core import actors, kernel
from lino.core.menus import find_menu_item
from lino.sphinxcontrib.actordoc import menuselection_text
from pprint import pprint
from lino.utils.diag import visible_for
from lino.core.utils import full_model_name

from lino.core.menus import Menu
from lino.core.actions import ShowTable

test_client = Client()
# naming it simply "client" caused conflict with a
# `lino_welfare.pcsw.models.Client`

import collections
HttpQuery = collections.namedtuple(
    'HttpQuery',
    ['username', 'url_base', 'json_fields', 'expected_rows', 'kwargs'])

settings.SITE.is_testing = True

def get_json_dict(username, uri, an='detail', **kwargs):
    url = '/api/{0}?fmt=json&an={1}'.format(uri, an)
    for k, v in kwargs.items():
        url += "&{}={}".format(k, v)
    test_client.force_login(rt.login(username).user)
    res = test_client.get(url, REMOTE_USER=username)
    assert res.status_code == 200
    return json.loads(res.content.decode())


def get_json_soup(username, uri, fieldname, **kwargs):
    """Being authentified as `username`, perform a web request to `uri` of
    the test client.

    """
    d = get_json_dict(username, uri, **kwargs)
    html = d['data'][fieldname]
    return BeautifulSoup(html, 'lxml')


def post_json_dict(username, url, data, **extra):
    """Send a POST with given username, url and data. The client is
    expected to respond with a JSON encoded response. Parse the
    response's content (which is expected to contain a dict), convert
    this dict to an AttrDict before returning it.

    """
    test_client.force_login(rt.login(username).user)
    res = test_client.post(url, data, REMOTE_USER=username, **extra)
    if res.status_code != 200:
        raise Exception("{} gave status code {} instead of 200".format(
            url, res.status_code))
    return AttrDict(json.loads(res.content.decode()))


def check_json_result(response, expected_keys=None, msg=''):
    """Checks the result of response which is expected to return a
    JSON-encoded dictionary with the expected_keys.

    """
    # print("20150129 response is %r" % response.content)
    if response.status_code != 200:
        raise Exception(
            "Response status ({0}) was {1} instead of 200".format(
                msg, response.status_code))
    try:
        result = json.loads(response.content.decode())
    except ValueError as e:
        raise Exception("{0} in {1}".format(e, response.content))
    if expected_keys is not None:
        if set(result.keys()) != set(expected_keys.split()):
            raise Exception("'{0}' != '{1}'".format(
                ' '.join(list(result.keys())), expected_keys))
    return result


def demo_get(
        username, url_base, json_fields=None,
        expected_rows=None, **kwargs):
    case = HttpQuery(username, url_base, json_fields,
                     expected_rows, kwargs)
    # Django test client does not like future pseudo-unicode strings
    # See #870
    url = str(settings.SITE.buildurl(case.url_base, **case.kwargs))
    # print(20160329, url)
    if False:
        msg = 'Using remote authentication, but no user credentials found.'
        try:
            response = test_client.get(url)
            raise Exception("Expected '%s'" % msg)
        except Exception:
            pass
            #~ self.tc.assertEqual(str(e),msg)
            #~ if str(e) != msg:
                    #~ raise Exception("Expected %r but got %r" % (msg,str(e)))

    if False:
        # removed 20161202 because (1) it was relatively useless and
        # (2) caused a PermissionDenied warning
        response = test_client.get(url, REMOTE_USER=str('foo'))
        if response.status_code != 403:
            raise Exception(
                "Status code %s other than 403 for anonymous on GET %s" % (
                    response.status_code, url))
    ses= rt.login(username)
    test_client.force_login(ses.user)
    response = test_client.get(url, REMOTE_USER=username)
    # try:
    if True:
        # user = settings.SITE.user_model.objects.get(
        #     username=case.username)
        result = check_json_result(
            response, case.json_fields,
            "GET %s for user %s" % (url, ses.user))

        num = case.expected_rows
        if num is not None:
            if not isinstance(num, tuple):
                num = [num]
            if result['count'] not in num:
                msg = "%s got %s rows instead of %s" % (
                    url, result['count'], num)
                raise Exception(msg)

    # except Exception as e:
    #     print("%s:\n%s" % (url, e))
    #     raise


def screenshot(obj, filename, rstname, username='robin'):
    """Insert a screenshot of the detail window for the given database
    object.

    Usage example in the source code of
    http://xl.lino-framework.org/specs/holidays.html.

    Problems: doesn't seem to wait long enough and
    therefore produces a white .png file.

    How to specify the filename? the current directory when doctest is
    running is normally the project root, but that's not sure. Best
    place would be the same directory as the rst file, but how to know
    that name from within a tested snippet?

    """
    from lino.api.selenium import Album, runserver

    assert filename.endswith('.png')
    assert rstname.endswith('.rst')

    ar = rt.login(renderer=dd.plugins.extjs.renderer)
    ba = obj.get_detail_action()
    uri = ar.get_detail_url(ba.actor, obj.pk)
    print(uri)

    def f(driver):
        app = Album(driver)
        driver.get("http://127.0.0.1:8000" + uri)
        # driver.get(uri)
        app.stabilize()
        if not driver.get_screenshot_as_file(filename):
            app.error("Failed to create {0}".format(filename))

    runserver(settings.SETTINGS_MODULE, f)


def show_menu_path(spec, language=None):
    """
    Print the menu path of the given actor or action.

    Deprecated.  You should rather use
    :meth:`lino.core.requests.BaseRequest.show_menu_path` which
    automatically sets the language of the user and works for any user
    type.
    """
    user_type = rt.models.users.UserTypes.get_by_value('900')
    mi = user_type.find_menu_item(spec)
    if mi is None:
        raise Exception("Invalid spec {0}".format(spec))
    if language:
        with translation.override(language):
            print(menuselection_text(mi))
    else:
        print(menuselection_text(mi))

    # items = [mi]
    # p = mi.parent
    # while p:
    #     items.insert(0, p)
    #     p = p.parent
    # return " --> ".join([i.label for i in items])


def noblanklines(s):
    """Remove blank lines from output. This is used to increase
    readability when some expected output would otherweise contain
    disturbing `<BLANKLINE>` which are not relevant to the test
    itself.

    """
    return '\n'.join([ln for ln in s.splitlines() if ln.strip()])


def show_choices(username, url, show_count=False):
    """Print the choices returned via web client."""
    test_client.force_login(rt.login(username).user)
    response = test_client.get(url, REMOTE_USER=username)
    if response.status_code != 200:
        raise Exception(
            "Response status ({0}) was {1} instead of 200".format(
                url, response.status_code))

    result = json.loads(response.content.decode())
    for r in result['rows']:
        print(r['text'])
        # print(r['value'], r['text'])

    if show_count:
        print("{} rows".format(result['count']))

from django.db.models import Model
from lino.core.actions import Action
from lino.core.tables import AbstractTable
from lino.core.boundaction import BoundAction

def show_workflow(actions, all=False, language=None):
    """
    Show the given actions as a table.  Usage example in
    :ref:`avanti.specs.cal`.

    """
    def doit():
        cells = []
        cols = ["Action name", "Verbose name", "Help text",
                "Target state", "Required states"]  # , "Required roles"]
        for a in actions:
            ht = a.help_text or ''
            if ht or all:
                # required_roles = ' '.join(
                #     [str(r) for r in a.required_roles])
                cells.append(
                    [a.action_name, a.label, unindent(ht),
                     a.target_state, a.required_states or '',
                     # required_roles
                    ])
        print(table(cols, cells).strip())

    if language:
        with translation.override(language):
            return doit()
    return doit()


def show_fields(model, fieldnames=None, columns=False, all=None):
    """
    Print an overview description of the specified fields of the
    specified model.

    If model is an action or table, print the parameter fields of that
    action or table.

    If model is a table and you want the columns instead of the
    parameter fields, then specify `columns=True`.

    By default this shows only fields which have a help text.  If you
    specify `all=True`, then also fields that have no help text will
    be shown.
    """
    cells = []
    cols = ["Internal name", "Verbose name", "Help text"]
    if all is None:
        all = fieldnames is not None
    if isinstance(model, BoundAction):
        get_field = model.action.parameters.get
        if fieldnames is None:
            fieldnames = model.action.params_layout
    elif isinstance(model, Action):
        get_field = model.parameters.get
        if fieldnames is None:
            fieldnames = model.params_layout.main
    elif issubclass(model, Model):
        get_field = model._meta.get_field
        # get_field = model.get_data_elem
        if fieldnames is None:
            fieldnames = [f.name for f in model._meta.get_fields()]
    elif issubclass(model, AbstractTable):
        if columns:
            get_field = model.get_data_elem
            if fieldnames is None:
                fieldnames = model.column_names
                # get_handle().list_layout.main.columns
        else:
            get_field = model.parameters.get
            if fieldnames is None:
                fieldnames = model.params_layout.main
    if isinstance(fieldnames, str):
        fieldnames = fieldnames.split()
    for n in fieldnames:
        fld = get_field(n)
        if fld is not None and hasattr(fld, 'verbose_name'):
            ht = fld.help_text or ''
            if ht or all:
                cells.append([n,
                              fld.verbose_name,
                              unindent(ht)])

    print(table(cols, cells).strip())

def show_fields_by_type(fldtype):
    """Print a list of all fields (in all models) that have the specified type.
    """
    from lino.core.utils import (sorted_models_list)
    items = []
    for model in sorted_models_list():
        flds = []
        for f in model._meta.fields:
            if isinstance(f, fldtype):
                name = f.name
                verbose_name = force_text(f.verbose_name).strip()
                txt = "{verbose_name} ({name})".format(**locals())
                flds.append(txt)
        if len(flds):
            txt = "{model} : {fields}".format(
                model=full_model_name(model), fields=", ".join(flds))
            items.append(txt)
    print(rstgen.ul(items))


def show_columns(*args, **kwargs):
    """Like :func:`show_fields` but with `columns` defaulting to True.

    """
    kwargs.update(columns=True)
    return show_fields(*args, **kwargs)


def py2rst(x, doctestfmt=True):
    return diag.py2rst(x, doctestfmt)


def show_dialog_actions():
    return analyzer.show_dialog_actions(True)


def walk_menu_items(username=None, severe=True):
    """Walk through all menu items which run a :class:`ShowTable
    <lino.core.actions.ShowTable>` action, showing how many data rows
    the grid contains.

    """
    def doit(ar):
        if ar is None:
            user_type = None
        else:
            user_type = ar.user.user_type
            test_client.force_login(ar.user)
        mnu = settings.SITE.get_site_menu(user_type)
        items = []
        for mi in mnu.walk_items():
          if mi.bound_action:
            if isinstance(mi.bound_action.action, ShowTable):
                mt = mi.bound_action.actor
                url = 'api/{}/{}'.format(mt.app_label, mt.__name__)
                url = str(settings.SITE.buildurl(url, fmt='json'))

                item = menuselection_text(mi) + " : "
                try:
                    response = test_client.get(url, REMOTE_USER=str(username))
                    result = check_json_result(
                        response, None,
                        "GET %s for user %s" % (url, username))
                    item += str(result['count'])
                except Exception as e:
                    if severe:
                        raise
                    else:
                        item += str(e)
                items.append(item)

        s = rstgen.ul(items)
        print(s)

    if settings.SITE.user_types_module:
        ar = settings.SITE.login(username)
        with translation.override(ar.user.language):
            doit(ar)
    else:
        doit(None)


def show_sql_queries():
    """
    Print the SQL queries which have been made since last call.

    Usage example: :ref:`specs.noi.sql`.
    """
    for qry in connection.queries:
        sql = qry['sql'].strip()
        print(sql.replace('"', ''))
    # reset_sql_queries()


def show_sql_summary(**kwargs):
    """Print a summary of the SQL queries which have been made since last
    call.

    Usage example: :ref:`specs.tera.sql`.

    """
    def func():
        for qry in connection.queries:
            try:
                yield "({time}) {sql};".format(**qry)
            except KeyError as e:
                yield "{} : {}".format(qry, e)

    sql_summary(func(), **kwargs)
    # reset_sql_queries()


def add_call_logger(owner, name):
    """Replace the callable named name on owner by a wrapper which
    additionally prints a message on each call.

    """
    func = getattr(owner, name)
    msg = "{}() on {} was called".format(name, owner)
    def w(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    setattr(owner, name, w)

def str2languages(txt):
    """
    Return a list of all translations for the given translatable text.
    """
    lst = []
    for lng in settings.SITE.languages:
        with translation.override(lng.django_code):
            lst.append(str(txt))
    return lst

def show_choicelist(cls):
    """
    Similar to :func:`rt.show`, but the `text` is shown in all
    languages instead of just the current language.
    """
    headers = ["value", "name"] + [lng.name for lng in settings.SITE.languages]
    rows = []
    for i in cls.get_list_items():
        row = [i.value, i.name] + str2languages(i.text)
        rows.append(row)
    print(table(headers, rows))

def show_choicelists():
    """
    Show all the choicelists defined in this application.
    """
    headers = ["name", "#items", "preferred_width"] + [lng.name for lng in settings.SITE.languages]
    rows = []
    for i in sorted(kernel.CHOICELISTS.values(), key=lambda s: str(s)):
        row = [str(i), len(i.choices), i.preferred_width] + str2languages(i.verbose_name_plural)
        rows.append(row)
    print(table(headers, rows))


def show_permissions(*args):
    print(visible_for(*args))


def show_quick_search_fields(*args):
    for m in args:
        print(str(m._meta.verbose_name_plural))
        for fld in m.quick_search_fields:
            print("- {} ({})".format(fld.verbose_name, fld.name))

def pprint_json_string(s):
    """
    Used to doctest json values and have them be python 2/3 passable.
    :param s: json string

    """
    print(json.dumps(json.loads(s),
                     indent=2,
                     sort_keys=True,
                     separators=(",", ": ")))
