def noop():
   pass

def win_asterisk():
   winsound.PlaySound('Asterisk',\
                      winsound.SND_ALIAS | winsound.SND_ASYNC)

try:
   import winsound 
   asterisk = win_asterisk
except ImportError:
   asterisk = noop



