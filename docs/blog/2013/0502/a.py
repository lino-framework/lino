# trying to exhaust memory during import
import time
L = []
while True:
    L.append(time.time())
    if not len(L) % 100000: 
        print len(L)
