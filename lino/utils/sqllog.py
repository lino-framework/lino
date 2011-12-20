## Copyright 2009-2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

from django.db import connection
from django.template import Template, Context


class SQLLogMiddleware:
    """
    Log all SQL statements direct to the console.
    Intended for use with the django development server.

    Based on http://djangosnippets.org/snippets/1672/
    but writes to a file on the server instead of to the response.

    """

    def process_response ( self, request, response ): 
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
        html = t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time}))
        html = html.replace('FROM','<b>FROM</b>')
        file('sqllog.html','w').write(html.encode('utf-8'))
        return response
        
class SQLLogToConsoleMiddleware:
    """
    Log all SQL statements to the console.
    Intended for use with the django development server.

    Based on http://djangosnippets.org/snippets/1672/ 
    but removed the test for settings.DEBUG.
    """
    def process_response(self, request, response): 
        if connection.queries:
            time = sum([float(q['time']) for q in connection.queries])        
            t = Template("{{count}} quer{{count|pluralize:\"y,ies\"}} in {{time}} seconds:\n\n{% for sql in sqllog %}[{{forloop.counter}}] {{sql.time}}s: {{sql.sql|safe}}{% if not forloop.last %}\n\n{% endif %}{% endfor %}")
            print t.render(Context({'sqllog':connection.queries,'count':len(connection.queries),'time':time}))                
        return response


class ShortSQLLogToConsoleMiddleware:
    """
    Log a summary of the SQL statements made to the console.
    Intended for use with the django development server.

    """
    def process_response(self, request, response): 
        if connection.queries:
            time = sum([float(q['time']) for q in connection.queries])
            t = Template("{{count}} quer{{count|pluralize:\"y,ies\"}} in {{time}} seconds")
            print t.render(Context({'count':len(connection.queries),'time':time}))                
        return response
