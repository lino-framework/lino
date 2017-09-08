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
    """Prints a parsed sql log nicely"""
    kw['sql'] = ("\n    ").join(textwrap.wrap(kw['sql'], sql_width))
    print("time: {time}\n"
          "table: {table}\n"
          "sql: {sql}".format(**kw))


if __name__ == "__main__":
    matches = []
    regex = r"^.+\((?P<time>[\d\.]*)\) (?P<sql>.*FROM \`(?P<table>.*?)\`.*)$"
    # f = open("log/lino.log", 'r')
    f = sys.stdin
    d= {}
    l = f.readline()
    while l:
        m = re.match(regex, l)
        # print m
        if m:
            g = m.groupdict()
            if d.get(g['table'], {'time':-1}) < g['time']:
                d[g['table']] = g
        l = f.readline()
    if d:
        for kw in d.values():
            p(kw)
            print "-------------------"
        print("The slowest SQL call was:")
        #find max
        kw = d[max(d, key=lambda x: float(d[x].get('time', 0)))]
        p(kw)
        print "-------------------"

    else:
        print("No sql queries found")