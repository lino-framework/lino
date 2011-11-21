# coding: latin1
# Snakelets for lino
from snakeserver.snakelet import Snakelet
from widgets import Window #, Grid, Label, Button, MenuBar, Editor, Form
from httpui import HttpUI
from lino.misc.compat import *
from lino.adamo.html import HtmlRenderer


class SnakeRenderer(HtmlRenderer):
   
   """ A SnakeRenderer lives only during MenuSnakelet.serve().  It
   refers to the request and the response which are valid only during
   this time.  """
   
   def __init__(self,ui,snakelet,request,response):
      HtmlRenderer.__init__(self,ui)
      # self._snakelet = snakelet
      # self._response = response
      # self._request = request
      self.wr = response.getOutput().write
      self.getURL = snakelet.getURL
      self.escape = snakelet.escape

		

class MainSnakelet(Snakelet):
   
   def serve(self, request, response):
		
      self.addNoCacheHeaders(response) # Lino pages cannot be cached...
      sc = request.getSessionContext()
      ui = getattr(sc,"ui",None)
      if ui is None:
         ui = sc.ui = HttpUI(request.getWebApp().getConfigItem('db'))
         
      r = SnakeRenderer(ui,self,request,response)
      
      frm = request.getForm()
		win = None
      try:
         w = frm['w']
      except KeyError:
         ui.message("no window specified")
         win = ui.getMainWindow()
      else:
         try:
            win = ui.getWindow(int(w))
         except IndexError:
            win = ui.getMainWindow()
         else:
            ui.message("window %s has been specified" % w)
            # a = requested action
            try:
               a = frm['a'] # action id
               ui.message("requested action "+a)
            except KeyError:
               pass
               # ui.message("no action requested")
               # simply display the requested window
            else:
               # win.renderedActions contains the list of actions of the
               # calling window. This list has been constructed during
               # renderWindow
               ra = win.renderedActions[int(a)]
               newWindow = ra.action.execute(ui)
               if newWindow is not None:
               # if isinstance(newWindow,Window):
                  win = newWindow
                  
      ui.setCurrentWindow(win)
      r.renderWindow(win)
      win.renderedActions = r.getRenderedActions()



