from lino.sdoc.styles import getDefaultStyleSheet
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame

import unittest 

class MyCase(unittest.TestCase):

   def setUp(self):
      
      styles = getDefaultStyleSheet()
      self.story = []
      self.story.append(
         Paragraph("This is a first paragraph",styles.Normal))
      self.story.append(
         Paragraph("This is <i>another</i> paragraph.", styles.Normal))

      self.assertEqual(len(self.story),2)
      
   
   def test01(self):
      """A Frame consumes the story while rendering.
      But this can be avoided by using list(story)
      """
      c = Canvas('test01.pdf')
      f = Frame(inch, inch, 2*inch, 9*inch, showBoundary=1)
      f.addFromList(list(self.story),c)
      self.assertEqual(len(self.story),2)

      f = Frame(4*inch, inch, 2*inch, 9*inch, showBoundary=1)
      f.addFromList(self.story,c)
      self.assertEqual(len(self.story),0)

      c.save()


   def test02(self):
      "What happens if a Frame gets full?"
      c = Canvas('test02.pdf')
      "create a very small frame:"
      f = Frame(inch, inch, inch, inch, showBoundary=1)
      f.addFromList(self.story,c)
      """
      The Frame takes from the list all elemens that fit into the Frame.
      """
      self.assertEqual(len(self.story),1)
      c.save()

      
