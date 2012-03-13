# -*- coding: UTF-8 -*-
import os
import os.path
import sys

from appy.pod.renderer import Renderer
from appy import version

#~ print "appy.version.verbose", version.verbose
#~ print "Python sys.version_info", sys.version
#~ print "Python sys.platform", sys.platform

APPY_PARAMS = dict()

#~ ACTIVE_TESTS = None # run all tests
ACTIVE_TESTS = [ 15 ] # run only specified tests

#~ APPY_PARAMS.update(ooPort=8100)
#~ APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\LIBREO~1\program\python.exe')

from lino.utils.appy_pod import setup_renderer

#~ try:
  #~ from lino.utils.restify import install_restify
#~ except ImportError:
  #~ def install_restify(*args):
      #~ pass

def run_test(number,title,XHTML=None,RST=None,HTML=None):
    if ACTIVE_TESTS and not number in ACTIVE_TESTS: 
        print "Skipped test #%d" % number
        return
    print "Running test #%d" % number
    tpl = os.path.join(os.path.abspath(os.path.dirname(__file__)),'test_template.odt')
    context = dict(locals())
    context.update(
        appy_version=version.verbose,
        python_version=sys.version,
        platform=sys.platform,
    )
    target = 'test_result_%d.odt' % number
    if os.path.exists(target): 
        os.remove(target)
    renderer = Renderer(tpl, context, target,**APPY_PARAMS)
    setup_renderer(renderer) # adds functions restify() and html()
    renderer.run()  
    print "Generated file", target
    #~ os.startfile(target)    


#~ # 1 : 
run_test(1,"Simple test. Works fine with version 0.6.6", '''
<div class="document">
<p>Hello, world?</p>
</div>
''')

#~ # 2 : 
run_test(2,"List items are not rendered (Appy 0.6.6)",'''
<div class="document">
<p>Some <strong>bold</strong> and some <em>italic</em> text.</p>
<p>A new paragraph.</p>
<p>A list with three items:</p>
<ul> 
<li>the first item</li> 
<li>another item</li> 
<li>the last item</li> 
</ul> 
<p>A last paragraph.</p>
</div>
''')
    
# 3 : 
run_test(3,"Same as 2, but using `restify` to make the XHTML",RST=u'''
Some **bold** and some *italic* text. 

A new paragraph.

A list with three items:

- the first item
- another item
- the last item

A last paragraph.
''')

run_test(5,"SAX parser error on Python 2.6",RST=u"""
Some **bold** and some *italic* text.

A new paragraph, followed by a list with three items.

- the first item
- another item
- the last item<

A last paragraph with some special characters like <, & and >.
""")


xhtml = """
<div class="section" id="titel">
<h1>Title</h1>
<div class="system-message">
<p class="system-message-title">System Message: WARNING/2 (<tt class="docutils">&lt;string&gt;</tt>, line 2)</p>
<p>Title underline too short.</p>
<pre class="literal-block">
Title
====
</pre>
</div>
</div>
"""
run_test(6,"20110516",XHTML=xhtml)

xhtml = """
<pre>
Title
====
</pre>
"""
run_test(7,"20110517",xhtml)

# http://lino.saffre-rumma.net/blog/2011/0525.html
html = """
<p><span class="Apple-style-span" style="font-size: 13px; line-height: 19px; font-family: sans-serif;">Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</span></p>
<p><span class="Apple-style-span" style="font-size: 20px; font-weight: bold;">A heading</span></p>
<p><span class="Apple-style-span" style="font-size: 13px; line-height: 19px; font-family: sans-serif;">Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</span></p>
"""
run_test(8,"20110525",HTML=html)


#~ # 9 : 
run_test(9,"Same as 2, but without wrapping <DIV>",HTML='''
<p>Some <strong>bold</strong> and some <em>italic</em> text.</p>
<p>A new paragraph.</p>
<p>A list with three items:</p>
<ul> 
<li>the first item</li> 
<li>another item</li> 
<li>the last item</li> 
</ul> 
<p>A last paragraph.</p>
''')
    
#~ # 10 : 

run_test(10,"TABLE",HTML='''
<table border="1">
  <colgroup>
    <col width="20" />
    <col width="100" />
    <col width="320" />
  </colgroup>
  <tr>
    <td>1. Zeile, 1. Spalte</td>
    <td>1. Zeile, 2. Spalte</td>
    <td>1. Zeile, 3. Spalte</td>
  </tr>
  <tr>
    <td>2. Zeile, 1. Spalte</td>
    <td>2. Zeile, 2. Spalte</td>
    <td>2. Zeile, 3. Spalte</td>
  </tr>
</table>
''')
    
#~ # 11 : 

html = '''
<table border="1" rules="groups">
  <thead>
    <tr>
      <th>Assoziation 1</th>
      <th>Assoziation 2</th>
      <th>Assoziation 3</th>
    </tr>
  </thead>
  <tfoot>
    <tr>
      <td><i>betroffen:<br>4 Mio. Menschen</i></td>
      <td><i>betroffen:<br>2 Mio. Menschen</i></td>
      <td><i>betroffen:<br>1 Mio. Menschen</i></td>
    </tr>
  </tfoot>
  <tbody>
  %s
  </tbody>
</table>
'''
rows = '''
<tr>
  <td>Berlin</td>
  <td>Hamburg</td>
  <td>M&uuml;nchen</td>
</tr><tr>
  <td>Milj&ouml;h</td>
  <td>Kiez</td>
  <td>Bierdampf</td>
</tr><tr>
  <td>Buletten</td>
  <td>Frikadellen</td>
  <td>Fleischpflanzerl</td>
</tr>
'''

html = html % (rows *20)

run_test(11,"TABLE 2 with head and foot",HTML=html)

#~ # 12 : 

#
import cgi
from lino.utils.htmlgen import UL
items = '''un deux trois
quatre cinq
siz sept huit'''.splitlines()
cells = []
cells.append('''<p>BISA</p>'''+UL(items))
cells.append('''<p>RCYCLE</p>'''+UL(items))
html = '<h1>%s</h1>' % cgi.escape(u"Le douzième essai")
#~ head = ''.join(['<col width="30" />' for c in cells])
#~ head = '<colgroup>%s</colgroup>' % head
s = ''.join(['<td valign="top">%s</td>' % c for c in cells])
s = '<tr>%s</tr>' % s
#~ s = head + s
html += '<table border="1" width="100%%">%s</table>' % s
html = '<div class="htmlText">%s</div>' % html
run_test(12,"TABLE 3",HTML=html)


#~ # 13 : 

html = """
<p>Appy.pod fails to render paragraphs 
inside a <strong>blockquote</strong> tag:</p>
<blockquote>
<p>This text is not rendered.</p>
</blockquote>

<p>Same for DIVs inside a <strong>blockquote</strong> tag:</p>
<blockquote>
<div>This text is not rendered.</div>
</blockquote>

<p>Only flowing text passes :</p>
<blockquote>
This text is rendered.
</blockquote>
"""
run_test(13,"20110723",HTML=html)

#~ # 14 : 

html = """
<TABLE>
<TR><TD width="20">foo</TD><TD width="100">bar</TD></TR>
</TABLE>
"""
run_test(14,"20120211",XHTML=html)

#~ # 15 : 

html = u"""
<p>bla bla</p>
<blockquote>
<table border="1" class="docutils">
<colgroup>
<col width="29%" />
<col width="71%" />
</colgroup>
<thead valign="bottom">
<tr><th class="head">terav</th>
<th class="head">pehme</th>
</tr>
</thead>
<tbody valign="top">
<tr><td><strong>s</strong>upp</td>
<td><strong>z</strong>oom</td>
</tr>
<tr><td><strong>\u0161</strong>okk</td>
<td><strong>\u017e</strong>urnaal, <strong>\u017e</strong>anre</td>
</tr>
</tbody>
</table>
</blockquote>
"""
run_test(15,"20120311",XHTML=html)
# explanation: the blockquote around our table disturbs. when removed, everything is okay

