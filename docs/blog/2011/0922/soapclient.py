from ZSI.client import Binding
fp = open('debug.out', 'a')
#~ b = Binding(url='/cgi-bin/simple-test', tracefile=fp)
b = Binding(url='http://127.0.0.1', tracefile=fp)
a = b.average(range(1,11))
assert a == 5
print b.hello()
fp.close()
