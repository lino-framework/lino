import win32ui
import win32con
import win32print

# fetch info about default printer:
printerName=win32print.GetDefaultPrinter()
h=win32print.OpenPrinter(printerName)
d=win32print.GetPrinter(h,2)
devmode=d['pDevMode']
info= [ "%s=%r" % (n,getattr(devmode,n))
        for n in dir(devmode)
        if n != 'DriverData' and n[0]!='_']
win32print.ClosePrinter(h)

inch = 1440.0
mm = inch / 25.4
DELTA=10

dc = win32ui.CreateDC()
dc.CreatePrinterDC()
dc.StartDoc("testjob")
dc.SetMapMode(win32con.MM_TWIPS)
x1,y1 = dc.GetWindowOrg()
x2,y2 = dc.GetWindowExt()

fontDict=dict(name="Courier New", height=200)
font = win32ui.CreateFont(fontDict)
dc.SelectObject(font)

# draw 10 rectangles as border
for i in range(10):
    d=int(i*mm)
    # move to upper left
    dc.MoveTo((x1+DELTA+d,-y1-DELTA-d))
    # line to upper right
    dc.LineTo((x2-DELTA-d,-y1-DELTA-d))

    # line to lower right
    dc.LineTo((x2-DELTA-d,-y2+DELTA+d))

    # line to lower left
    dc.LineTo((x1+DELTA+d,-y2+DELTA+d))

    # line to upper left
    dc.LineTo((x1+DELTA+d,-y1-DELTA-d))

# print info
x=int(x1+30*mm)
y=int(-y1-30*mm)
dx,dy = dc.GetTextExtent(" ")
for ln in info:
    dc.TextOut(x,y,ln)
    y -= dy
        
dc.EndDoc()
