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

SKIP_TESTS = range(6) 

#~ APPY_PARAMS.update(ooPort=8100)
#~ APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\LIBREO~1\program\python.exe')

try:
  from lino.utils.restify import install_restify
except ImportError:
  def install_restify(*args):
      pass

def run_test(number,title,HTML,RST=None):
    if number in SKIP_TESTS: 
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
    install_restify(renderer)
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
run_test(3,"Same as 2, but using `restify` to make the HTML",None,u'''
Some **bold** and some *italic* text. 

A new paragraph.

A list with three items:

- the first item
- another item
- the last item

A last paragraph.
''')

run_test(5,"SAX parser error on Python 2.6",None,u"""
Some **bold** and some *italic* text.

A new paragraph, followed by a list with three items.

- the first item
- another item
- the last item<

A last paragraph with some special characters like <, & and >.
""")


html = """
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
run_test(6,"20110516",html)
