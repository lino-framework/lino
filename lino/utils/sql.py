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
    print(
          "table: {table}\n"
          "Longest_time: {time}\n"
          "Queries: {count}\n"
          "total_time: {total_time}\n"
          "sql: {sql}".format(**kw))


if __name__ == "__main__":
    matches = []
    regex = r"^.+?\((?P<time>[\d\.]*)\) (?P<sql>.*FROM \`(?P<table>.*?)\`.*?;).*$"
    # f = open("log/lino.log", 'r')
    f = sys.stdin
    d= {}
    l = f.readline()
    while l:
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
        l = f.readline()
    if d:
        for kw in sorted(d.values(), key= lambda x: x['total_time']):
            p(kw)
            print "-------------------"
        print("The slowest SQL call was:")
        #find max
        kw = d[max(d, key=lambda x: float(d[x].get('time', 0)))]
        p(kw)
        print "-------------------"

    else:
        print("No sql queries found")