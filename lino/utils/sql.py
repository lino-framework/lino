# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""Print a summary of a series of SQL queries.

If invoked from command line, expects as argument the log file to be
parsed.

"""

from __future__ import print_function

# import lino
# lino.startup('lino_book.projects.noi1e.settings.demo')
# import django
# print django.__file__
# from lino.api.doctest import *
# show_sql_queries()
# #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
# r = demo_get('robin','api/tickets/AllTickets', fmt='json', limit=1)
# print(r)
# show_sql_queries()


import re
import sys
import textwrap
import rstgen


def p(kw, sql_width=60):
    # Prints a parsed sql log nicely
    print(
        "table: {table}\n"
        "Longest_time: {time}\n"
        "Queries: {count}\n"
        "total_time: {total_time}".format(kw))
    sql = "{sql1} {table} {sql2}".format(kw)
    sql = sql.replace('"', '')
    kw['sql'] = ("\n    ").join(textwrap.wrap(sql, sql_width))
    print("sql: {sql}".format(kw))


# regex = r"^.+?\((?P<time>[\d\.]*)\) (?P<sql>.*FROM \`(?P<table>.*?)\`.*?;).*$"

# regex_select = r"^.*?\((?P<time>\S+?)\)\s+SELECT\s+(?P<sql1>.*)\s+FROM\s+(?P<table>\S+)\s*(?P<sql2>.*);$"

# regex_delete = r"^.*?\((?P<time>\S+?)\)\s+DELETE FROM\s+(?P<table>\S+)\s*(?P<sql2>.*);$"

# regex_insert = r"^.*?\((?P<time>\S+?)\)\s+INSERT INTO\s+(?P<table>\S+)\s*(?P<sql2>.*);$"

# regex_begin = r"^.*?\((?P<time>\S+?)\)\s+BEGIN;$"

# operations = [
#     ('select', regex_select),
#     ('delete', regex_delete),
#     ('insert', regex_insert),
#     ('begin', regex_begin)
# ]

regex = r"^.*?\((?P<time>\S+?)\)\s+(?P<sql>.*);$"

try:

    import sqlparse
    from sqlparse.sql import IdentifierList, Identifier
    from sqlparse.tokens import Keyword, DML

except ImportError:

    sqlparse = None


# Copied from https://github.com/andialbrecht/sqlparse/blob/master/examples/extract_table_names.py


def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def extract_from_part(parsed):
    from_seen = False
    for item in parsed.tokens:
        if from_seen:
            if is_subselect(item):
                for x in extract_from_part(item):
                    yield x
            elif item.ttype is Keyword:
                return
            else:
                yield item
        elif item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True


def extract_table_identifiers(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                yield identifier.get_name()
        elif isinstance(item, Identifier):
            yield item.get_name()
        # It's a bug to check for Keyword here, but in the example
        # above some tables names are identified as keywords...
        elif item.ttype is Keyword:
            yield item.value

def extract_tables(stmt):
    stream = extract_from_part(stmt)
    return list(extract_table_identifiers(stream))


class Entry(object):
    def __init__(self, sql, time):
        self.sql = sql
        self.time = float(time)
        self.total_time = self.time
        self.count = 1
        self.table = ''

        stmt = sqlparse.parse(sql)[0]
        self.stmt_type = stmt.get_type()
        tables = extract_tables(stmt)
        if len(tables):
            self.table = tables[0]

        # for token in stmt:
        #     if isinstance(token, Identifier):
        #         self.table = str(token)
        #         break

    def group_key(self):
        return self.table + ' ' + self.stmt_type

    def collect(self, other):
        self.total_time += other.time
        self.time = max(self.time, other.time)
        self.count += 1


def sql_summary(lines, show_times=False, show_details=False, **options):
    """
    Parse the SQL queries from `lines` and print a summary.

    `lines` is an iterable of text lines from a logfile or from
    :func:`lino.api.doctest.show_sql_summary`.

    Any backticks and double quotes are removed for readability.
    MySQL uses backticks where SQLite uses double quotes around table
    and field names in the SQL syntax.  `Here
    <https://stackoverflow.com/questions/11321491/when-to-use-single-quotes-double-quotes-and-backticks-in-mysql>`__
    is an interesting discussion with examples.
    """
    if sqlparse is None:
        raise Exception("sql_summary() requires the sqlparse package")
    # matches = []
    d = {}
    for l in lines:
        l = l.replace('"', '')
        l = l.replace('`', '')

        m = re.match(regex, l)
        if m:
            g = m.groupdict()
            entry = Entry(g['sql'], g['time'])
            k = entry.group_key()
            if k in d:
                d[k].collect(entry)
            else:
                d[k] = entry
        else:
            raise Exception("Invalid line {!r}".format(l))

        # k = None
        # for op, regex in operations:
        #     m = re.match(regex, l)
        #     if m:
        #         g = m.groupdict()
        #         k = g['table'] + op
        #         g['operation'] = op
        #         break

        # if k:
        #     g['time'] = float(g['time'])
        #     r = d.setdefault(k, {})
        #     r['count'] = r.get('count', 0) + 1
        #     r["total_time"] = r.get("total_time", 0 ) + float(g['time'])
        #     if r.get('time', -1) < g['time']:
        #         d[k].update(g)
        # else:
        #     raise Exception("Invalid line {!r}".format(l))

    if d:
        if show_details:
            for e in sorted(d.values(), key=lambda x: x.total_time):
                p(e, **options)
                print("-------------------")
            print("The slowest SQL call was:")
            # find max
            e = d[max(d, key=lambda x: x.time)]
            p(e, **options)
            print("-------------------")
        else:
            if show_times:
                headers = 'total_time count table stmt_type time'.split()
                values = sorted(d.values(), key=lambda x: -x.total_time)
            else:
                headers = 'table stmt_type count'.split()
                values = sorted(d.values(), key=lambda x: x.table)
            rows = []
            for e in values:
                rows.append([getattr(e, h) for h in headers])
                rows.sort()
            print(rstgen.table(headers, rows))
    else:
        print("No sql queries found")


if __name__ == "__main__":
    # f = open("log/lino.log", 'r')
    f = sys.stdin
    sql_summary(f.readlines(), show_details=True)
