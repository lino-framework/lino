import sound

def confirm(prompt,answer="y",allowed="yn"):
   sound.asterisk()
   while True:
      s = raw_input(prompt+" [y,n]")
      if s == "":
         s = answer
      s = s.lower()
      if s == "y":
         return True
      if s == "n":
         return False


def notify(msg):
   
   """Notify the user about something just for information.

   Without acknowledgment request.

   examples: why a requested action was not executed
   """
   sound.asterisk()
   notifier(msg)

def console_notify(msg):
   print '[note] ' + msg
   
notifier = console_notify

