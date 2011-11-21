# based on Examples in http://pywebsvcs.sourceforge.net/zsi.html

def hello():
    return "Hello, world"

def echo(*args):
    return args

def average(*args):
    print args
    sum = 0
    for i in args: sum += i
    return sum / len(args)

from ZSI import dispatch
dispatch.AsServer()