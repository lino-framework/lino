try:
  True
except NameError:
  True, False = 1, 0

try:
   file
except NameError:
   file = open
   
def _(x):
   return x
