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

def p(kw, sql_width = 60):
    # Prints a parsed sql log nicely
    kw['sql'] = ("\n    ").join(textwrap.wrap(kw['sql'], sql_width))
    print(
          "table: {table}\n"
          "Longest_time: {time}\n"
          "Queries: {count}\n"
          "total_time: {total_time}\n"
          "sql: {sql}".format(**kw))

regex = r"^.+?\((?P<time>[\d\.]*)\) (?P<sql>.*FROM \`(?P<table>.*?)\`.*?;).*$"

# regex = r".*\((?P<time>[\d\.]*)\) (?P<sql>.*FROM \`(?P<table>.*?)\`.*?;).*"

def sql_summary(lines):
    """Parse the SQL queries from `lines` and print a summary.

    `lines` is an iterable of text lines from a logfile or from 
    :func:`lino.api.doctest.show_sql_summary`.

    """
    # matches = []
    d = {}
    for l in lines:
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
            print("Invalid line: " + l)
        
    if d:
        for kw in sorted(d.values(), key= lambda x: x['total_time']):
            p(kw)
            print("-------------------")
        print("The slowest SQL call was:")
        #find max
        kw = d[max(d, key=lambda x: float(d[x].get('time', 0)))]
        p(kw)
        print("-------------------")

    else:
        print("No sql queries found")


if __name__ == "__main__":
    # f = open("log/lino.log", 'r')
    f = sys.stdin
    sql_summary(f.readlines())
    
        
