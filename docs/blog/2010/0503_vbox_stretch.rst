= 20100503_vbox_stretch =

Please have a look at the [http://code.google.com/p/lino/source/browse/extjs-showcases/20100503_vbox_stretch.html Source code] of the showcase that demonstrates my problem.

It opens a Window with a single item (a FormPanel) with vbox layout and 3 items; the third item (which contains a htmleditor) has stretch:1, the others have stretch:0. My problem is that the second item (country, region and email) takes too much height. At least when using Firefox:

<table>
<tr>
<td>
Here is a screenshot of the result (Firefox 3.6.3 on Windows XP) :

<p align="center">
<a href="http://lino.googlecode.com/hg/screenshots/20100503.jpg">
<img src="http://lino.googlecode.com/hg/screenshots/20100503.jpg" width="90%"/>
</a></p>
</td>
<td>

On IE the same showcase renders as expected:

<p align="center">
<a href="http://lino.googlecode.com/hg/screenshots/20100503b.jpg">
<img src="http://lino.googlecode.com/hg/screenshots/20100503b.jpg" width="90%"/>
</a></p>
</td>
</tr>
</table>

I'm using ExtJS version 3.2.1.

Am I doing something forbidden? Is there a workaround for this problem? 