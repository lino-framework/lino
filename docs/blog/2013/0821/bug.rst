`xhtml()` doesn't like `<div>` inside a `<span>`
================================================

You should be able run the snippets on this page and reproduce the problem
by downloading files :file:`bug.rst` and :file:`0821.odt` from 
:srcref:`/docs/blog/2013/0821` into a folder of your choice 
and then running::

  $ python -m doctest bug.rst

:file:`0821.odt` contains a simple `appy pod from clause 
<http://appyframework.org/podWritingAdvancedTemplates.html>`_::

  do text
  from xhtml(chunk)

We are going to render this into a file :file:`out.odt`:

>>> OUTFILE = 'out.odt'

Alternatively you might try to render to a `.pdf` file if you have an 
openoffice or libreoffice server running on port 2002 (uncomment the 
following line in your copy of :file:`bug.rst`):

>>> # OUTFILE = 'out.pdf'

When `chunk` is the following, then it works:

>>> html = u'<p><div><span>it works!</span></div></p>'

But when I inverse the nesting (`<div>` inside `<span>`) 
then it fails:

>>> html = u'<p><span><div>Oops</div></span></p>'

The following snippet will render it:

>>> import os
>>> from appy.pod.renderer import Renderer
>>> html = html.encode('utf-8')
>>> context = dict(chunk=html)
>>> if os.path.exists(OUTFILE):
...     os.remove(OUTFILE)
>>> r = Renderer('0821.odt',context,OUTFILE)
>>> r.run()
>>> os.path.exists(OUTFILE)
True

The file `out.odt` now exists, but it contains invalid `content.xml`
and LibreOffice will complain when you try to open it.


I originally wrote this page for Gaëtan in the hope that he will 
fix this bug in appy pod... but then I understood:
in fact Appy Pod is right! 

A `<div>` inside a `<span>` is no valid XHTML.
According to 
`Mac on stackoverflo <http://stackoverflow.com/questions/2919909/nesting-div-within-span-problem>`_
"several websites use this method for styling",
but the bug is not in Gaëtan's `renderXhtml` method, 
it is in own code: in :mod:`lino.utils.html2xhtml`.






