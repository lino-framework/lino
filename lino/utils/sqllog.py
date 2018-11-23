# Copyright 2009-2011 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""A middleware for sending SQL statements to the Lino logger.
Intended for use with the django development server.


"""
from __future__ import print_function
from builtins import object

from django.db import connection
from django.template import Template, Context


class SQLLogMiddleware(object):

    """
    Log all SQL statements direct to the console.

    Based on http://djangosnippets.org/snippets/1672/
    but writes to a file on the server instead of to the response.
    """

    def process_response(self, request, response):
        time = 0.0
        for q in connection.queries:
            time += float(q['time'])

        t = Template('''<html><body>
            <p><em>Total query count:</em> {{ count }}<br/>
            <em>Total execution time:</em> {{ time }}</p>
            <ul class="sqllog">
                {% for sql in sqllog %}
                    <li>{{ sql.time }}: {{ sql.sql }}</li>
                {% endfor %}
            </ul>
            </body></html>
        ''')

        #~ response.content = "%s%s" % ( response.content, t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time})))
        html = t.render(
            Context({'sqllog': connection.queries, 'count': len(connection.queries), 'time': time}))
        html = html.replace('FROM', '<b>FROM</b>')
        file('sqllog.html', 'w').write(html.encode('utf-8'))
        return response


class SQLLogToConsoleMiddleware(object):

    """
    Log all SQL statements to the console.
    Intended for use with the django development server.

    Based on http://djangosnippets.org/snippets/1672/
    but removed the test for settings.DEBUG.
    """

    def process_response(self, request, response):
        if connection.queries:
            time = sum([float(q['time']) for q in connection.queries])
            t = Template(
                "{{count}} quer{{count|pluralize:\"y,ies\"}} in {{time}} seconds:\n\n{% for sql in sqllog %}[{{forloop.counter}}] {{sql.time}}s: {{sql.sql|safe}}{% if not forloop.last %}\n\n{% endif %}{% endfor %}")
            print(t.render(Context({'sqllog': connection.queries, 'count': len(connection.queries), 'time': time})))
        return response


class ShortSQLLogToConsoleMiddleware(object):

    """
    Log a summary of the SQL statements made to the console.
    Intended for use with the django development server.

    """

    def process_response(self, request, response):
        if connection.queries:
            time = sum([float(q['time']) for q in connection.queries])
            t = Template(
                "{{count}} quer{{count|pluralize:\"y,ies\"}} in {{time}} seconds")
            print(t.render(Context({'count': len(connection.queries), 'time': time})))
        return response
