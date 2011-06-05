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
ACTIVE_TESTS = (9,) # run only specified tests

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
    
