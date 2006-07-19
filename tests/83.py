#coding: latin1
## Copyright 2003-2006 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
"""
from lino.misc.tsttools import TestCase, main
from lino.gendoc import html


class Case(TestCase):

    def memo2xml(self,memo,xml):
        doc=html.HtmlDocument()
        doc.body.memo(memo)
        self.assertEquivalent(doc.body.toxml(),xml)
    
    def test01(self):
        self.memo2xml("""

<table>
<tr>
<td>foo</td>
<td>bar</td>
<td>baz</td>
</tr>
<tr>
<td>A</td>
<td>B</td>
<td>C</td>
</tr>
</table>

        ""","""
<BODY><TABLE><TR><TD>foo</TD><TD>bar</TD><TD>baz</TD></TR><TR><TD>A</TD><TD>B</TD><TD>C</TD></TR></TABLE></BODY>
        """)
        self.memo2xml("""
        
<table>
<tr>
<td>foo
<td>bar
<td>baz
<tr>
<td>A
<td>B
<td>C
</table>
    
        ""","""
<BODY><TABLE><TR><TD>foo
</TD><TD>bar
</TD><TD>baz
</TD></TR><TR><TD>A
</TD><TD>B
</TD><TD>C
</TD></TR></TABLE></BODY>
        """)

        self.memo2xml("""
    
About character formatting:
<em>emphasized</em> is same as <i>italic</i>.

<i>italic</i>, <b>bold</b> and <b><i>bold-italic</i></b>
are implemented using separate fonts, while
<sup>superscript</sup> simply raises the baseline.

Now the same text in underlined:
<u>
<i>italic</i>, <b>bold</b> and <b><i>bold-italic</i></b>
are implemented using separate fonts, while
<sup>superscript</sup> simply raises the baseline.
</u>

        ""","""
        
<BODY><P>
About character formatting:
<EM>emphasized</EM> is same as <I>italic</I>.</P><P><I>italic</I>, <B>bold</B> and <B><I>bold-italic</I></B>
are implemented using separate fonts, while
<SUP>superscript</SUP> simply raises the baseline.</P><P>Now the same text in underlined:
<U>
<I>italic</I>, <B>bold</B> and <B><I>bold-italic</I></B>
are implemented using separate fonts, while
<SUP>superscript</SUP> simply raises the baseline.
</U></P></BODY>

        """)
        
        self.memo2xml("""
        
        <img src="test.jpg">
        
        ""","""
        
        <BODY><IMG src="test.jpg"/></BODY>
        
        """)
        
        self.memo2xml("""
        blablabla, blabla & bla:

        <ul>
        <li>foo
        <li>bar
        <li>bazz
        </ul>
        ""","""
        <BODY><P>
        blablabla, blabla &amp; bla:</P><UL><LI>foo
        </LI><LI>bar
        </LI><LI>bazz
        </LI></UL></BODY>
        """)

        self.memo2xml("""
        <ul>
        <li>This is the first list item.

        And this is another paragraph in the first list item.

        <li>This is the second list item.
        </ul>
        ""","""
<BODY><UL><LI>This is the first list item.<P>
And this is another paragraph in the first list
item.</P></LI><LI>This is the second list item.
        </LI></UL></BODY>
        """)

        self.memo2xml("""
        Price: 25,- &euro;
        """,u"""\
<BODY><P>
        Price: 25,- &#8364;
        </P></BODY>""")


        self.memo2xml("""

<tt>This</tt> memo starts with formatted text.
        
        ""","""
        
<BODY><P><TT>This</TT> memo starts with formatted text.
</P></BODY>

        """)
        
        self.memo2xml("""
        
<table class="EmptyTable">
<tr><td align="left">
(Left header)
<td align="right">
(Right header)
</table>
    
        ""","""
        
<BODY><TABLE class="EmptyTable"><TR><TD align="left">
(Left header)
</TD><TD align="right">
(Right header)
</TD></TR></TABLE></BODY>
    
        """)
        
        self.memo2xml("""
        ""","""
        <BODY/>
        """)
        
        
        

                
if __name__ == '__main__':
    main()

