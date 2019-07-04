# -*- coding: UTF-8 -*-
# Copyright 2006-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""See introduction in :doc:`/dev/memo`.

TODO:

- the auto-completer might insert the full text into the editor after the
  pattern. The user can then decide whether to leave it or not.

- The memo commands might also be defined as suggesters with a trigger of type
  "[ticket ". Note that in that case we need to add a new attribute "suffix"
  which would be empty for # and @ but "]" for memo commands.

"""
from __future__ import unicode_literals

from builtins import str
from builtins import object
import logging ; logger = logging.getLogger(__name__)
# from inspect import getsourcefile
import re
import inspect

from etgen import etree
# from django.db import models

COMMAND_REGEX = re.compile(r"\[(\w+)\s*((?:[^[\]]|\[.*?\])*?)\]")
#                                       ===...... .......=

EVAL_REGEX = re.compile(r"\[=((?:[^[\]]|\[.*?\])*?)\]")


class Suggester(object):
    """

    Holds the configuration for the behaviour of a given "trigger".

    Every value of :attr:`Parser.suggesters` is an instance of this.


    """
    def __init__(self, trigger, data, fldname, formatter=str, getter=None):
        self.trigger = trigger
        self.data = data
        self.fldname = fldname
        self.formatter = formatter

        fld = data.model._meta.get_field(fldname)

        # if isinstance(fld, models.IntegerField):
        #     searchkw = {}

        if getter is None:
            def getter(abbr):
                return data.get(**{fldname: abbr})

        self.getter = getter

    def get_suggestions(self, query=''):
        flt = self.data.model.quick_search_filter(query)
        for obj in self.data.filter(flt)[:5]:
            yield (getattr(obj, self.fldname), self.formatter(obj))

    def get_object(self, abbr):
        return self.getter(abbr)


class Parser(object):
    """The memo parser.

    Every Lino site has a global memo parser stored in
    :attr:`lino.core.site.Site.kernel.memo_parser`.

    """

    safe_mode = False

    def __init__(self, **context):
        self.commands = dict()
        self.context = context
        self.renderers = dict()
        self.suggesters = dict()

    def add_suggester(self, *args, **kwargs):

        """

        `trigger` is a short text, usually one character, like "@" or "#",
        which will trigger a list of autocomplete suggestions to pop up.

        `func` is a callable expected to yield a series of suggestions to be
        displayed in text editor.

        Every suggestion is expected to be a tuple `(abbr, text)`, where `abbr` is
        the abbreviation to come after the trigger (e.g. a username or a ticket
        number), and text is a full description of this suggestion to be displayed
        in the list.

        Usage examples: see :mod:`lino_xl.lib.tickets` and :mod:`lino.modlib.users`

        """

        s = Suggester(*args, **kwargs)
        if s.trigger in self.suggesters:
            raise Exception("Duplicate suggester for {}".format(s.trigger))
        self.suggesters[s.trigger] = s

    def compile_suggester_regex(self):
        triggers = r"".join(["\\" if key in "[\^$.|?*+(){}" else "" + key for key in self.suggesters.keys()])
        return re.compile(r"([^\w])?([" + triggers + "])(\w+)")


    def register_command(self, cmd, func):
        # print("20170210 register_command {} {}".format(cmd, func))
        self.commands[cmd] = func

    def register_renderer(self, cl, func):
        # print("20181205", str(cl))
        # if str(cl).endswith("Person'>"):
        #     raise Exception("20181205")

        frame, filename, line_number, function_name, lines, index = \
        inspect.stack()[2]
        # print(frame, filename, line_number, function_name, lines, index)
        func._defined_in = "function {} in {}".format(function_name, filename)

        if cl in self.renderers:
            def fmt(x):
                return x._defined_in
            ex = self.renderers[cl]
            raise Exception(
                "Duplicate renderer for {} : {} and {}".format(
                    cl, fmt(ex), fmt(func)))
        self.renderers[cl] = func

    def register_django_model(
            self, name, model, cmd=None, rnd=None, title=str):
        """
        Register the given string `name` as command for referring to
        database rows of the given Django database model `model`.

        Optional keyword arguments are 

        - `cmd` the command handler used by :meth:`parse`
        - `rnd` the renderer function for :meth:`obj2memo`
        - `title` a function which returns a string to be used as title
        """
        # print("20170210 register_django_model {} {}".format(name, model))
        if rnd is None:
            def rnd(obj):
                return "[{} {}] ({})".format(name, obj.id, title(obj))
        if cmd is None:
            def cmd(parser, s):
                """
Insert a reference to the specified database object.

The first argument is mandatory and specifies the primary key.
All remaining arguments are used as the text of the link.

                """
                args = s.split(None, 1)
                if len(args) == 1:
                    pk = s
                    txt = None
                else:
                    pk = args[0]
                    txt = args[1]

                ar = parser.context['ar']
                kw = dict()
                # dd.logger.info("20161019 %s", ar.renderer)
                pk = int(pk)
                obj = model.objects.get(pk=pk)
                # try:
                # except model.DoesNotExist:
                #     return "[{} {}]".format(name, s)
                if txt is None:
                    txt = "#{0}".format(obj.id)
                    kw.update(title=title(obj))
                e = ar.obj2html(obj, txt, **kw)
                # return str(ar)
                return etree.tostring(e)

        self.register_command(name, cmd)
        self.register_renderer(model, rnd)
            
        
    def eval_match(self, matchobj):
        expr = matchobj.group(1)
        try:
            return self.format_value(eval(expr, self.context))
        except Exception as e:
            # don't log an exception because that might cause lots of
            # emails to the admins.
            # logger.warning(e)
            return self.handle_error(matchobj, e)

    def format_value(self, v):
        if etree.iselement(v):
            return str(etree.tostring(v))
        return str(v)

    def suggester_match(self, matchobj):
        whitespace = matchobj.group(1)
        whitespace = "" if whitespace is None else whitespace
        trigger = matchobj.group(2)
        abbr = matchobj.group(3)
        suggester = self.suggesters[trigger] # can't key error as regex is created from the keys
        ar = self.context["ar"]  # don't break silently
        try:
            obj = suggester.get_object(abbr)
            return whitespace + etree.tostring(ar.obj2html(obj, trigger+abbr, title=str(obj)))
        except Exception as e:
            # likely a mismatch or bad pk, return full match
            # return self.handle_error(matchobj, e)
            return matchobj.group(0)

    def cmd_match(self, matchobj):
        cmd = matchobj.group(1)
        cmdh = self.commands.get(cmd, None)
        if cmdh is None:
            return matchobj.group(0)

        params = matchobj.group(2)
        params = params.replace('\\\n', ' ')
        params = params.replace(u'\xa0', ' ')
        params = params.replace(u'\u200b', ' ')
        params = params.replace('&nbsp;', ' ')
        params = str(params.strip())
        try:
            return self.format_value(cmdh(self, params))
        except Exception as e:
            # logger.warning(e)
            # don't log an exception because that might cause lots of
            # emails to the admins.
            return self.handle_error(matchobj, e)

    def handle_error(self, mo, e):
        #~ return mo.group(0)
        msg = "[ERROR %s in %r at position %d-%d]" % (
            e, mo.group(0), mo.start(), mo.end())
        # logger.debug(msg)
        return msg

    def parse(self, s, **context):
        """
        Parse the given string `s`, replacing memo commands by their
        result.
        """
        self.context.update(context)
        if self.suggesters and 'ar' in self.context:
            suggester_regex = self.compile_suggester_regex()
            s = suggester_regex.sub(self.suggester_match, s)

        s = COMMAND_REGEX.sub(self.cmd_match, s)
        if not self.safe_mode:
            s = EVAL_REGEX.sub(self.eval_match, s)
        return s

    def obj2memo(self, obj, **options):
        """Render the given database object as memo markup.

        This works only for objects for which there is a renderer.
        Renderers are defined by :meth:`register_renderer`.

        """
        h = self.renderers.get(obj.__class__)
        if h is None:
            return "**{}**".format(obj)
        return h(obj, **options)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
