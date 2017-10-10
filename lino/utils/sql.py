# -*- coding: UTF-8 -*-
# Copyright 2017 Tonis Piip, Luc Saffre
# License: BSD (see file COPYING for details)
"""Print a summary of a series of SQL queries.

If invoked from command line, expects as argument the log file to be
parsed.

"""

from __future__ import print_function

# import lino
# lino.startup('lino_book.projects.team.settings.demo')
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
# from pprint import pprint
import textwrap
from atelier import rstgen

def p(kw, sql_width = 60):
    # Prints a parsed sql log nicely
    print(
          "table: {table}\n"
          "Longest_time: {time}\n"
          "Queries: {count}\n"
          "total_time: {total_time}".format(**kw))
    sql = "{sql1} {table} {sql2}".format(**kw)
    sql = sql.replace('"','')
    kw['sql'] = ("\n    ").join(textwrap.wrap(sql, sql_width))
    print("sql: {sql}".format(**kw))

# regex = r"^.+?\((?P<time>[\d\.]*)\) (?P<sql>.*FROM \`(?P<table>.*?)\`.*?;).*$"

regex = r"^.*?\((?P<time>\S+?)\)\s+(?P<sql1>.*)\s+FROM\s+(?P<table>\S+)\s*(?P<sql2>.*);$"


def sql_summary(lines, show_times=False, show_details=False, **options):
    """Parse the SQL queries from `lines` and print a summary.

    `lines` is an iterable of text lines from a logfile or from 
    :func:`lino.api.doctest.show_sql_summary`.

    Any backticks and double quotes are removed for readability.
    MySQL uses backticks where SQLite uses double quotes around table
    and field names in the SQL syntax.  `Here
    <https://stackoverflow.com/questions/11321491/when-to-use-single-quotes-double-quotes-and-backticks-in-mysql>`__
    is an interesting discussion with examples.

    """
    # matches = []
    d = {}
    for l in lines:
        l = l.replace('"','')
        l = l.replace('`','')
        m = re.match(regex, l)
        # print m
        if m:
            g = m.groupdict()
            g['time'] = float(g['time'])
            r = d.setdefault(g['table'], {})
            r['count'] = r.get('count', 0) + 1
            r["total_time"] = r.get("total_time", 0 ) + float(g['time'])
            if r.get('time', -1) < g['time']:
                d[g['table']].update(g)
        else:
            print("Invalid line {!r}".format(l))
        
    if d:
        if show_details:
            for kw in sorted(d.values(), key= lambda x: x['total_time']):
                p(kw, **options)
                print("-------------------")
            print("The slowest SQL call was:")
            #find max
            kw = d[max(d, key=lambda x: float(d[x].get('time', 0)))]
            p(kw, **options)
            print("-------------------")
        else:
            if show_times:
                headers = 'total_time count table time'.split()
                values = sorted(d.values(), key= lambda x: -x['total_time'])
            else:
                headers = 'table count'.split()
                values = sorted(d.values(), key= lambda x: x['table'])
            rows = []
            for kw in values:
                rows.append([kw[h] for h in headers])
            print(rstgen.table(headers, rows))
    else:
        print("No sql queries found")


if __name__ == "__main__":
    # f = open("log/lino.log", 'r')
    f = sys.stdin
    sql_summary(f.readlines(), show_details=True)
    
        
