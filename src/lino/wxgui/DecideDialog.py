"""      
   DecideDialog:
      +==========================================================+
      | +------------------------------------------------------+ |
      | | msgPanel                                             | |
      | |                                                      | |
      | |                                                      | |
      | |                                                      | |
      | |                                                      | |
      | +------------------------------------------------------+ |
      | +------------------------------------------------------+ |
      | | buttonPanel                                          | |
      | |  +---------+  +---------+  +---------+  +---------+  | |
      | |  | btn[0]  |  |         |  |         |  | btn[n]  |  | |
      | |  |         |  |         |  |         |  |         |  | |
      | |  +---------+  +---------+  +---------+  +---------+  | |
      | +------------------------------------------------------+ |
      +----------------------------------------------------------+
      
   the top sizer is vbox and contains msgPanel and buttonPanel
      
"""      

from wxPython.wx import *

class DecideDialog(wxDialog):
   """
   Displays a modal dialog with a question and N buttons, 1 for each Label
   in answers. Returns the index of the chosen button.
   """
   def __init__(self, parent, log, msg, label, answers):
      style=wxDEFAULT_DIALOG_STYLE | wxDIALOG_MODAL | wxRESIZE_BORDER
      #label = babel.tr(lino.Messages.text,msg)
      self.log = log
      wxDialog.__init__(self, parent, 
         -1, label, 
         wxDefaultPosition, 
         wxDefaultSize, 
         style, 
         label)
         
      self.SetBackgroundColour(wxRED) #wxNamedColour("MEDIUM ORCHID"))
      msgPanel = wxStaticText(self, -1,msg) #,wxDefaultPosition, wxDefaultSize)
      msgPanel.SetBackgroundColour(wxGREEN)
      buttonPanel = wxPanel(self,-1) #,wxDefaultPosition, wxDefaultSize)
      msgPanel.SetBackgroundColour(wxBLUE)
      
      vbox = wxBoxSizer(wxVERTICAL)
      vbox.Add(msgPanel,1,wxEXPAND|wxALL,10)
      vbox.Add(buttonPanel,1,wxEXPAND|wxALL,10)
      
      hbox = wxBoxSizer(wxHORIZONTAL)
      id = 10000
      for answer in answers:
         button = wxButton(buttonPanel,id,answer,
            wxDefaultPosition, wxDefaultSize)
         # If wxDefaultSize is specified then the button is sized 
         # appropriately for the text.

         self.log.write("button %s: size=(%s)\n" % (answer,
            button.GetSize()))
         hbox.Add(button, 1, wxALL,10)
         
         EVT_BUTTON(self, id, self.OnButton)
         id += 1
         

      self.SetAutoLayout( true ) # tell dialog to use sizer
      
      self.SetSizer( vbox )      # actually set the sizer
      
      buttonPanel.SetSizer( hbox )
      hbox.Fit(buttonPanel)
      
      vbox.Fit( self ) # set size to minimum size as calculated by the sizer
      #vbox.SetSizeHints( self ) # set size hints to honour mininum size
         
      self.Layout()
         
   def OnButton(self,event):
      self.log.write("event.GetId() : %d\n" % event.GetId())
      # self.SetReturnCode()
      self.EndModal(event.GetId()-10000) 
      # self.Destroy()
      


#---------------------------------------------------------------------------

class TestFrame(wxFrame):
    def __init__(self, parent, log):
       self.log = log
       wxFrame.__init__(self, parent, -1, "DecideDialog")

       panel = wxPanel(self, -1)

       button = wxButton(panel, 1003, "Decide")
       button.SetPosition(wxPoint(15, 15))
       EVT_BUTTON(self, 1003, self.OnSelect)
       EVT_CLOSE(self, self.OnCloseWindow)


    def OnSelect(self, event):
      title = "Important question"
      msg = "Where do you want to go today?"
      answers = ("I don't know...","to restaurant?","to market?")
      dlg = DecideDialog(self,self.log,msg,title,answers)
      val = dlg.ShowModal()
      self.log.write("result : %d\n" % val)
      dlg.Destroy()
      

    def OnCloseWindow(self, event):
        self.Destroy()



#---------------------------------------------------------------------------

if __name__ == '__main__':
     import sys
     app = wxPySimpleApp()
     frame = TestFrame(None, sys.stdout)
     frame.Show(true)
     app.MainLoop()
 


    
