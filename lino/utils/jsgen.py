# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

r"""A framework for generating Javascript from Python.

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
  
Another example...

>>> def onReady(name):
...     yield js_line("hello = function() {")
...     yield js_line("console.log(%s)" % py2js("Hello, " + name + "!"))
...     yield js_line("}")
>>> print(py2js(onReady("World")))
hello = function() {
console.log("Hello, World!")
}
<BLANKLINE>

And yet another example (`/blog/2012/0208`)...

>>> chunk = '<a href="javascript:alert({&quot;record_id&quot;: 122 })">Test</a>'
>>> print(py2js(chunk))
"<a href=\"javascript:alert({&quot;record_id&quot;: 122 })\">Test</a>"

>>> data_record = dict(
...   title="Upload \"Aufenthaltserlaubnis\"",
...   data=dict(owner=chunk))
>>> print(py2js(data_record))
{ "data": { "owner": "<a href=\"javascript:alert({&quot;record_id&quot;: 122 })\">Test</a>" }, "title": "Upload \"Aufenthaltserlaubnis\"" }
>>> response = dict(
...   message="Upload \"Aufenthaltserlaubnis\" wurde erstellt.",
...   success=True,
...   data_record=data_record)
>>> print(py2js(response)) #doctest: +NORMALIZE_WHITESPACE
{ "data_record": { "data": { "owner": "<a href=\"javascript:alert({&quot;record_id&quot;: 122 })\">Test</a>" }, "title": "Upload \"Aufenthaltserlaubnis\"" }, "message": "Upload \"Aufenthaltserlaubnis\" wurde erstellt.", "success": true }

"""

from __future__ import unicode_literals
from builtins import str
from builtins import object

import logging
logger = logging.getLogger(__name__)

import types
import datetime
import decimal
import fractions
import threading


from django.conf import settings
import json
from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.db.models.fields import NOT_PROVIDED

from lino.utils import IncompleteDate
from lino.utils.quantities import Quantity
from lino.utils.xmlgen import etree
from lino.utils import curry
from lino.core.permissions import Permittable
from lino.core.permissions import make_view_permission_handler


user_profile_rlock = threading.RLock()

CONVERTERS = []


def dict2js(d):
    return ", ".join(["%s: %s" % (k, py2js(v)) for k, v in list(d.items())])


def register_converter(func):
    CONVERTERS.append(func)

_for_user_profile = None


def with_user_profile(profile, func, *args, **kwargs):
    """Run the given callable `func` with the given user profile `profile`
    activated. Optional args and kwargs are forwarded to the callable,
    and the return value is returned.

    """
    global _for_user_profile

    with user_profile_rlock:
        old = _for_user_profile
        _for_user_profile = profile
        return func(*args, **kwargs)
        _for_user_profile = old


def get_user_profile():
    return _for_user_profile

# def set_user_profile(up):
#     global _for_user_profile
#     _for_user_profile = up

# set_for_user_profile = set_user_profile


def key2js(s):
    if isinstance(s, str):
        return s
    return json.dumps(s)  # ,cls=DjangoJSONEncoder)


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
    """A Component is a Variable whose value is a dict of otpions.
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

    def __init__(self, name, **kw):
        Component.__init__(self, name)
        self.setup(**kw)
        # install `allow_read` permission handler:
        self.install_permission_handler()

    def install_permission_handler(self):
        self.allow_read = curry(make_view_permission_handler(
            self, True,
            self.debug_permissions,
            self.required_roles), self)

    def is_visible(self):
        if self.hidden:
            return False
        return self.get_view_permission(_for_user_profile)

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
            self.label = label
        if required_roles is not NOT_PROVIDED:
            if not isinstance(required_roles, set):
                raise Exception(
                    "20150628 %s has required_roles %s" % (
                        self, required_roles))
            self.required_roles = required_roles
        # if help_text is not None:
        #     self.help_text = help_text

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
        for sub in list(v.values()):
            for ln in declare_vars(sub):
                yield ln
        return
    if isinstance(v, VisibleComponent) and not v.get_view_permission(
            _for_user_profile):
        return
    if isinstance(v, Component):
        for sub in list(v.ext_options().values()):
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


def py2js(v):
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
        return "".join([py2js(x) for x in v])
    if etree.iselement(v):
        return json.dumps(etree.tostring(v))

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
        elems = [py2js(x) for x in v
                 if (not isinstance(x, VisibleComponent))
                 or x.get_view_permission(_for_user_profile)]
        return "[ %s ]" % ", ".join(elems)

    if isinstance(v, dict):
        # 20160423: removed "sorted(v.items())" because it caused
        # TypeError when the dictionary contained a mixture of unicode
        # and future.types.newstr objects.
        try:
            items = [
                i for i in sorted(v.items())
                if (not isinstance(v, VisibleComponent))
                or v.get_view_permission(_for_user_profile)]
        except TypeError as e:
            raise TypeError("Failed to sort {0} : {1}".format(v, e))
        return "{ %s }" % ", ".join(
            ["%s: %s" % (py2js(k), py2js(i)) for k, i in items])

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
            v = IncompleteDate(v)
            return '"%s"' % v.strftime(settings.SITE.date_format_strftime)
        return '"%s"' % v.strftime(settings.SITE.date_format_strftime)

    if isinstance(v, float):
        return repr(v)
    # return json.encoder.encode_basestring(v)
    # print repr(v)
    # http://docs.djangoproject.com/en/dev/topics/serialization/
    # if not isinstance(v, (str,unicode)):
        # raise Exception("20120121 %r is of type %s" % (v,type(v)))
    return json.dumps(v)
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
