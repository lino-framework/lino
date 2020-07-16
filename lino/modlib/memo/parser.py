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
import logging ; logger = logging.getLogger(__name__)

import re
import inspect

from etgen import etree

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

    def register_command(self, cmdname, func):
        """Register a memo command identified by the given text `cmd`.

        `func` is the ommand handler.  It must be a callable which will be
        called with two positional arguments `ar` and `params`.

        """
        # print("20170210 register_command {} {}".format(cmdname, func))
        self.commands[cmdname] = func

    def register_renderer(self, cl, func):
        """Register the given function `func` as a renderer for objects of class `cl`."""
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
            # raise Exception(
            #     "Duplicate renderer for {} : {} and {}".format(
            #         cl, fmt(ex), fmt(func)))
            # logger.info("Ignore duplicate renderer for {} : {} and {}".format(
            #        cl, fmt(ex), fmt(func)))
            # Ignore silently
            return
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
            def cmd(ar, s):
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

                # ar = parser.context.get('ar', None)
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

    def eval_match_func(self, context):
        def func(matchobj):
            expr = matchobj.group(1)
            try:
                return self.format_value(eval(expr, context))
            except Exception as e:
                # don't log an exception because that might cause lots of
                # emails to the admins.
                # logger.warning(e)
                return self.handle_error(matchobj, e)
        return func

    def format_value(self, v):
        if etree.iselement(v):
            return str(etree.tostring(v))
        return str(v)

    def get_referred_objects(self, text):
        """Yield all database objects referred in the given `text` using a suggester.
        """
        regex = self.compile_suggester_regex()
        all_matchs = re.findall(regex, text)
        for match in all_matchs:
            suggester = self.suggesters[match[1]]
            try:
                yield suggester.get_object(match[2])
            except Exception:
                pass  #

    def suggester_match_func(self, ar):

        def func(matchobj):
            whitespace = matchobj.group(1)
            whitespace = "" if whitespace is None else whitespace
            trigger = matchobj.group(2)
            abbr = matchobj.group(3)
            suggester = self.suggesters[trigger] # can't key error as regex is created from the keys
            try:
                obj = suggester.get_object(abbr)
                return whitespace + etree.tostring(ar.obj2html(obj, trigger+abbr, title=str(obj)))
            except Exception as e:
                # likely a mismatch or bad pk, return full match
                # return self.handle_error(matchobj, e)
                return matchobj.group(0)
        return func

    def cmd_match_func(self, ar):

        def func(matchobj):
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
                return self.format_value(cmdh(ar, params))
            except Exception as e:
                # logger.warning(e)
                # don't log an exception because that might cause lots of
                # emails to the admins.
                return self.handle_error(matchobj, e)
        return func

    def handle_error(self, mo, e):
        #~ return mo.group(0)
        msg = "[ERROR %s in %r at position %d-%d]" % (
            e, mo.group(0), mo.start(), mo.end())
        # logger.debug(msg)
        return msg

    def parse(self, src, ar=None, context=None):
        """
        Parse the given string `src`, replacing memo commands by their
        result.

        `ar` is the action request asking to parse. User permissions and
        front-end renderer of this request apply.

        `context` is a dict of variables to make available when parsing
        expressions in safe mode.

        """
        if self.suggesters:
            regex = self.compile_suggester_regex()
            mf = self.suggester_match_func(ar)
            src = regex.sub(mf, src)

        src = COMMAND_REGEX.sub(self.cmd_match_func(ar), src)
        if not self.safe_mode:
            # run-time context overrides the global parser context
            ctx = dict()
            ctx.update(self.context)
            if context is not None:
                ctx.update(context)
            ctx.update(ar=ar)
            src = EVAL_REGEX.sub(self.eval_match_func(ctx), src)
        return src

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
