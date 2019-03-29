# -*- coding: UTF-8 -*-
# Copyright 2009-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

r"""A framework for generating Javascript from Python.

See also :doc:`/specs/jsgen`.

Example:

>>> class TextField(Component):
...    declare_type = DECLARE_VAR
>>> class Panel(Component):
...    declare_type = DECLARE_VAR
>>> fld1 = TextField(fieldLabel="Field 1", name='fld1', xtype='textfield')
>>> fld2 = TextField(fieldLabel="Field 2", name='fld2', xtype='textfield')
>>> fld3 = TextField(fieldLabel="Field 3", name='fld3', xtype='textfield')
>>> p1 = Panel(title="Panel",name='p1', xtype='panel', items=[fld2, fld3])
>>> main = Component(title="Main", name='main', xtype='form', items=[fld1, p1])
>>> d = dict(main=main, wc=[1, 2, 3])

>>> for ln in declare_vars(d):
...   print(ln)
var fld11 = { "fieldLabel": "Field 1", "xtype": "textfield" };
var fld22 = { "fieldLabel": "Field 2", "xtype": "textfield" };
var fld33 = { "fieldLabel": "Field 3", "xtype": "textfield" };
var p14 = { "items": [ fld22, fld33 ], "title": "Panel", "xtype": "panel" };

>>> print(py2js(d))
{ "main": { "items": [ fld11, p14 ], "title": "Main", "xtype": "form" }, "wc": [ 1, 2, 3 ] }

"""

from __future__ import unicode_literals
from builtins import str
from builtins import object
from future.types import newstr
import six

import logging
logger = logging.getLogger(__name__)

import types
import datetime
import decimal
import fractions


from django.conf import settings
import json
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.db.models.fields import NOT_PROVIDED

from lino.utils import IncompleteDate
from lino.utils.quantities import Quantity
from etgen import etree
from lino.utils import curry
from lino.core.permissions import Permittable
from lino.core.permissions import make_view_permission_handler
from lino.modlib.users.utils import get_user_profile
from lino.modlib.users.utils import with_user_profile  # backwards compat


CONVERTERS = []


def dict2js(d):
    return ", ".join(["%s: %s" % (k, py2js(v)) for k, v in d.items()])

def obj2dict(o, attrs):
    """

    :param o: object
    :param attrs: space seperated string or list of strings of wanted attrs
    :param kws: existing dict of values
    :return: dict with key:value pairs that match the object[arrts] if arrts exist in object
    """
    result = dict()
    if type(attrs) != list:
        attrs = attrs.split(" ")

    for k in attrs:
        if hasattr(o, k):
            result[k] = getattr(o, k)
    return result


def register_converter(func):
    CONVERTERS.append(func)



# def key2js(s):
#     if isinstance(s, str):
#         return s
#     return json.dumps(s)  # ,cls=DjangoJSONEncoder)


def id2js(s):
    return s.replace('.', '_')


class js_code(object):

    "A string that py2js will represent as is, not between quotes."

    def __init__(self, s):
        self.s = s
    # def __repr__(self):
        # return self.s


def js_line(s, *args):
    return js_code(s + '\n', *args)

DECLARE_INLINE = 0
DECLARE_VAR = 1
DECLARE_THIS = 2


class Value(object):

    declare_type = DECLARE_INLINE
    value_template = "%s"

    def __init__(self, value):
        self.value = value

    def js_declare(self):
        return []

    def subvars(self):
        return []

    # def js_before_body(self):
        # for v in self.subvars():
            # for ln in v.js_before_body():
                # yield ln
    def js_body(self):
        for v in self.subvars():
            for ln in v.js_body():
                yield ln

    # def js_after_body(self):
        # for v in self.subvars():
            # for ln in v.js_after_body():
                # yield ln

    def as_ext(self):
        return self.value_template % py2js(self.value)


VARIABLE_COUNTER = 0


class Variable(Value):
    declare_type = DECLARE_INLINE
    ext_suffix = ''
    name = None
    ext_name = None

    def __init__(self, name, value):

        global VARIABLE_COUNTER
        VARIABLE_COUNTER += 1
        if name is None:
            self.ext_name = "var%s%d" % (self.ext_suffix, VARIABLE_COUNTER)
        else:
            name = str(name)
            self.ext_name = "%s%s%d" % (
                id2js(name), self.ext_suffix, VARIABLE_COUNTER)
        Value.__init__(self, value)
        # assert self.declare_type != DECLARE_INLINE

        self.name = name
        # if name is None:
            # assert self.declare_type == DECLARE_INLINE
            # ~ #self.name = "unnamed %s" % self.__class__.__name__
        # else:
            # self.name = name
            # self.ext_name = id2js(name) + self.ext_suffix
        # self.ext_name = id2js(name) + self.ext_suffix

    def __str__(self):
        # if self.ext_name is None: raise Exception("20120920"+str(self.name))
        # assert self.ext_name is not None
        return self.ext_name

    def js_declare(self):
        yield "// begin js_declare %s" % self
        yield "// declare subvars of %s" % self
        for v in self.subvars():
            for ln in v.js_declare():
                yield ln
        yield "// end declare subvars of %s" % self
        value = self.js_value()
        if self.declare_type == DECLARE_INLINE:
            pass
        elif self.declare_type == DECLARE_VAR:
            yield "var %s = %s;" % (self.ext_name, value)
        elif self.declare_type == DECLARE_THIS:
            yield "this.%s = %s;" % (self.ext_name, value)
        yield "// end js_declare %s" % self

    # def js_column_lines(self):
        # return []

    def as_ext(self):
        if self.declare_type == DECLARE_INLINE:
            return self.js_value()
        if self.declare_type == DECLARE_THIS:
            return "this." + self.ext_name
        return self.ext_name

    def js_value(self):
        return self.value_template % py2js(self.value)


class Component(Variable):
    """
    A Component is a Variable whose value is a dict of options.
    Deserves more documentation.
    """

    def __init__(self, name=None, **options):
        # note that we remove the "**" from options ;-)
        Variable.__init__(self, name, options)

    def js_value(self):
        value = self.ext_options()
        return self.value_template % py2js(value)

    def ext_options(self, **kw):
        kw.update(self.value)
        return kw

    def update(self, **kw):
        if 'label' in kw:
            raise Exception("20181023")
        self.value.update(**kw)

    def remove(self, *keys):
        for k in keys:
            if k in self.value:
                del self.value[k]

    def walk(self):
        """Walk over this component and its children."""
        items = self.value['items']
        if not isinstance(items, (list, tuple)):
            items = [items]
        for i in items:
            for e in i.walk():
                if e.is_visible():
                    yield e


class VisibleComponent(Component, Permittable):
    """A visible component
    """
    vflex = False
    hflex = True
    width = None
    height = None
    preferred_width = 10
    preferred_height = 1
    # help_text = None
    # flex = None
    hidden = False
    _label = None

    def __init__(self, name, **kwargs):
        Component.__init__(self, name)
        self.setup(**kwargs)
        # self.install_permission_handler()
        # if name == "overview":
        #     print("20181022", kwargs)

    def install_permission_handler(self):
        """Define the `allow_read` handler used by
        :meth:`get_view_permission`.  This must be done only once, but
        after having configured :attr:`debug_permissions` and
        :attr:`required_roles`.

        """
        self.allow_read = curry(make_view_permission_handler(
            self, True,
            self.debug_permissions,
            self.required_roles), self)

    def is_visible(self):
        if self.hidden:
            return False
        return self.get_view_permission(get_user_profile())

    def get_view_permission(self, profile):
        return self.allow_read(profile)

    def setup(self, width=None, height=None, label=None,
              preferred_width=None,
              # help_text=None,
              required_roles=NOT_PROVIDED,
              **kw):
        self.value.update(kw)
        # Component.__init__(self,name,**kw)
        if preferred_width is not None:
            self.preferred_width = preferred_width
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if label is not None:
            self._label = label
        if required_roles is not NOT_PROVIDED:
            if not isinstance(required_roles, set):
                raise Exception(
                    "20150628 %s has required_roles %s" % (
                        self, required_roles))
            self.required_roles = required_roles
        # if help_text is not None:
        #     self.help_text = help_text
        self.install_permission_handler()

    def get_label(self):
        return self._label

    def set_label(self, v):
        self._label = v

    def __str__(self):
        "This shows how elements are specified"
        name = Component.__str__(self)
        if self.width is None:
            return name
        if self.height is None:
            return name + ":%d" % self.width
        return name + ":%dx%d" % (self.width, self.height)

    def unused__repr__(self):
        return str(self)

    def pprint(self, level=0):
        return ("  " * level) + str(self)

    def walk(self):
        if self.is_visible():
            yield self

    def debug_lines(self):
        sep = u"</td><td>"
        cols = """ext_name name parent label __class__.__name__
        elements js_value
        label_align vertical width preferred_width height
        preferred_height vflex""".split()
        yield '<tr><td>' + sep.join(cols) + '</td></tr>'
        for e in self.walk():
            yield '<tr><td>' + sep.join([py2html(e, n) for n in cols]) + '</td></tr>'

    def ext_options(self, **kw):
        kw = Component.ext_options(self, **kw)
        # edge case of invalid extjs layout when user doesn't have permision to view vflex items. Ticket #2916
        if getattr(self, 'vflex', False) and kw.get('region', "") != "center" and \
                get_user_profile() and \
                len([e for e in getattr(getattr(self, 'parent',None), "elements",[])
                     if e.get_view_permission(get_user_profile())]) == 1:
            kw['region'] = 'center'
        return kw

def declare_vars(v):
    """
    Yields the Javascript lines that declare the given  :class:`Variable` `v`.
    If `v` is a :class:`Component`, `list`, `tuple` or `dict` which contains
    other variables, recursively yields also the lines to declare these.
    """
    if isinstance(v, (list, tuple)):
        for sub in v:
            for ln in declare_vars(sub):
                yield ln
        return
    if isinstance(v, dict):
        for sub in v.values():
            for ln in declare_vars(sub):
                yield ln
        return
    if isinstance(v, VisibleComponent) and not v.get_view_permission(
            get_user_profile()):
        return
    if isinstance(v, Component):
        for sub in v.ext_options().values():
            for ln in declare_vars(sub):
                yield ln
        # DON'T return
    elif isinstance(v, Value):
        # 20120616 if not v.is_visible(): return
        # ok = True
        for ln in declare_vars(v.value):
            yield ln
        # DON'T return

    if isinstance(v, Variable):
        # 20120616 if not v.is_visible(): return
        if v.declare_type == DECLARE_VAR:
            yield "var %s = %s;" % (v.ext_name, v.js_value())
        elif v.declare_type == DECLARE_THIS:
            yield "this.%s = %s;" % (v.ext_name, v.js_value())


def py2js(v, compact=True):
    """Note that None values are rendered as ``null`` (not ``undefined``.

    """
    # assert _for_user_profile is not None
    # logger.debug("py2js(%r)",v)
    for cv in CONVERTERS:
        v = cv(v)

    # if isinstance(v,LanguageInfo):
        # return v.django_code

    if isinstance(v, Value):
        return v.as_ext()
        # v = v.as_ext()
        # if not isinstance(v, basestring):
            # raise Exception("20120121b %r is of type %s" % (v,type(v)))
        # return v
    if isinstance(v, Promise):
        # v = force_text(v)
        return json.dumps(force_text(v.encode('utf8')))

    if isinstance(v, types.GeneratorType):
        return "".join([py2js(x, compact=compact) for x in v])
    if etree.iselement(v):
        return json.dumps(force_text(etree.tostring(v)))
        # try:
        #     return json.dumps(force_text(etree.tostring(v)))
        # except Exception as e:
        #     return json.dumps("Failed to render {!r} : {}".format(v, e))

    # if type(v) is types.GeneratorType:
        # raise Exception("Please don't call the generator function yourself")
        # return "\n".join([ln for ln in v])
    if callable(v):
        # print 20120114, repr(v)
        # raise Exception("Please call the function yourself")
        return "\n".join([ln for ln in v()])
    if isinstance(v, js_code):
        return str(v.s)  # v.s might be a unicode
    if v is None:
        # return 'undefined'
        return 'null'
    if isinstance(v, (list, tuple)):  # (types.ListType, types.TupleType):
        elems = [py2js(x, compact=compact) for x in v
                 if (not isinstance(x, VisibleComponent))
                 or x.get_view_permission(get_user_profile())]
        sep = ", " if compact else ", \n"
        return "[ %s ]" % sep.join(elems)

    if isinstance(v, dict):
        items = [
            # i for i in sorted(v.items(), key=lambda x: str(x))
            # i for i in sorted(v.items())
            i for i in v.items()
            if (not isinstance(v, VisibleComponent))
            or v.get_view_permission(get_user_profile())]

        if six.PY2:
            # "sorted(v.items())" without sortkey caused TypeError when
            # the dictionary contained a mixture of unicode and
            # future.types.newstr objects.
            def sortkey(x):
                if isinstance(x[0], newstr):
                    return six.text_type(x[0])
                return x[0]
        else:
            def sortkey(x):
                return x[0]

        items = sorted(items, key=sortkey)
        # try:
        #     items = sorted(items, key=sortkey)
        # except TypeError as e:
        #     raise TypeError("Failed to sort {0!r} : {1}".format(items, e))
        sep = ", " if compact else ", \n"
        return "{ %s }" % sep.join(
            ["%s: %s" % (py2js(k, compact=compact), py2js(i, compact=compact)) for k, i in items])

    if isinstance(v, bool):  # types.BooleanType:
        return str(v).lower()
    if isinstance(v, Quantity):
        return '"%s"' % v
    if isinstance(v, (int, decimal.Decimal, fractions.Fraction)):
        return str(v)
    if isinstance(v, IncompleteDate):
        return '"%s"' % v.strftime(settings.SITE.date_format_strftime)
    if isinstance(v, datetime.datetime):
        return '"%s"' % v.strftime(settings.SITE.datetime_format_strftime)
    if isinstance(v, datetime.time):
        return '"%s"' % v.strftime(settings.SITE.time_format_strftime)
    if isinstance(v, datetime.date):
        if v.year < 1900:
            v = IncompleteDate.from_date(v)
            return '"%s"' % v.strftime(settings.SITE.date_format_strftime)
        return '"%s"' % v.strftime(settings.SITE.date_format_strftime)

    if isinstance(v, float):
        return repr(v)
    # return json.encoder.encode_basestring(v)
    # print repr(v)
    # http://docs.djangoproject.com/en/dev/topics/serialization/
    # if not isinstance(v, (str,unicode)):
        # raise Exception("20120121 %r is of type %s" % (v,type(v)))
    return json.dumps(v, sort_keys=True,
                  indent=4, separators=(',', ': ')
                      )
    # try:
    #     return json.dumps(v)
    # except TypeError as e:
    #     raise TypeError("%r : %s" % (v, e))
    # return json.dumps(v,cls=DjangoJSONEncoder) # http://code.djangoproject.com/ticket/3324


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
