import formatter
__note__ = """

i stopped this. I am not convinced that the formatter module suits
Lino's needs. If i continue: I must have a HtmlFormatter class (not
HtmlWriter class) because push_font and pop_font (e.g.) don't just
write new_font()

"""

writer = formatter.DumbWriter()

toUser = LinoFormatter(writer)
toSuperTitle = LinoFormatter(writer)
toMargin = LinoFormatter(writer)

   
def ToUserLog(msg):
   #userLog.send_literal_data(msg)
   toUser.send_flowing_data(msg)

def ToDebug(msg):
   #ToUserLog(msg)
      
#def ToSuperTitle(msg):
#   toSuperTitle.send_flowing_data(msg)
   
class LinoFormatter(formatter.AbstractFormatter):
   """
   - headers
   - table
   """

   def __init__(self,writer):
      formatter.AbstractFormatter.__init__(self,writer)
      self.headers = []
      self.sequences = []


class HtmlWriter(formatter.NullWriter):
    def __init__(self,out=None):
       self.out = out or sys.stdout
    def flush(self): pass
    def new_alignment(self, align): pass
    def new_font(self, font):
       size,i,b,tt = font
       self.out.write('')
    def new_margin(self, margin, level): pass
    def new_spacing(self, spacing): pass
    def new_styles(self, styles): pass
    def send_paragraph(self, blankline): pass
    def send_line_break(self): pass
    def send_hor_rule(self, *args, **kw): pass
    def send_label_data(self, data): pass
    def send_flowing_data(self, data): pass
    def send_literal_data(self, data): pass
   
