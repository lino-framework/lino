# thanks to http://newcenturycomputers.net/projects/pythonicwindowsprinting.html
import win32print
import win32gui
import win32ui
import win32con


#because we use MM_TWIPS:
inch = 1440.0
mm = inch / 25.4

jobName="test"
printerName=win32print.GetDefaultPrinter()
spoolFile=r"c:\tmp.ps"

# open the printer.
hprinter = win32print.OpenPrinter(printerName)
# retrieve default settings.  this code has complications on
# win95/98, I'm told, but I haven't tested it there.
props = win32print.GetPrinter(hprinter,2)
devmode=props["pDevMode"]

if devmode is None:
    # workaround, see http://lino.saffre-rumma.ee/news/477.html
    print "%r has no pDevMode property" % props
else:
    # change paper size and orientation
    # constants are available here:
    # http://msdn.microsoft.com/library/default.asp?\
    # url=/library/en-us/intl/nls_Paper_Sizes.asp
    devmode.PaperSize = win32con.DMPAPER_A4
    devmode.Orientation = win32con.DMORIENT_PORTRAIT

# create dc using new settings.
# first get the integer hDC value.
# note that we need the name.
dch = win32gui.CreateDC("WINSPOOL",
                        printerName,
                        devmode)
# next create a PyCDC from the hDC.
dc = win32ui.CreateDCFromHandle(dch)
dc.StartDoc(jobName,spoolFile)
dc.StartPage()


from lino.textprinter import devcaps 

print "LOGPIXELSX",dc.GetDeviceCaps(devcaps.LOGPIXELSX)
print "LOGPIXELSY",dc.GetDeviceCaps(devcaps.LOGPIXELSY)


devicex = dc.GetDeviceCaps(devcaps.LOGPIXELSX)
devicey = dc.GetDeviceCaps(devcaps.LOGPIXELSY)

def devicex2mm(pixels):
    inches = float(pixels) / devicex
    return inches * 25.4

def devicey2mm(pixels):
    inches = float(pixels) / devicey
    return inches * 25.4


print "HORZRES",devicex2mm(dc.GetDeviceCaps(devcaps.HORZRES)),"mm"
print "PHYSICALWIDTH",devicex2mm(dc.GetDeviceCaps(devcaps.PHYSICALWIDTH)),"mm"
print "PHYSICALOFFSETX",devicex2mm(dc.GetDeviceCaps(devcaps.PHYSICALOFFSETX)),"mm"

print "VERTRES",devicex2mm(dc.GetDeviceCaps(devcaps.VERTRES)),"mm"
print "PHYSICALHEIGHT",devicex2mm(dc.GetDeviceCaps(devcaps.PHYSICALHEIGHT)),"mm"
print "PHYSICALOFFSETY",devicex2mm(dc.GetDeviceCaps(devcaps.PHYSICALOFFSETY)),"mm"

        
dc.SetMapMode(win32con.MM_TWIPS)
#dc.SetViewportOrg((-1000,0))
        
org = dc.GetWindowOrg()
ext = dc.GetWindowExt()
print "org:",org
print "ext:",ext

def twips2mm(twips):
    return twips * 1440.0


fontDict=dict(name="Courier New",
              height=120)
font = win32ui.CreateFont(fontDict)
dc.SelectObject(font)
        
DELTA=10
LEFT=org[0]
RIGHT=ext[0]
TOP=org[1]
BOTTOM=ext[1]


LEFT=0
RIGHT=int(210*mm)
TOP=-int(297*mm)
BOTTOM=0

CS=int(9*mm) # Cross Size

# move to upper left
dc.MoveTo((LEFT,TOP))
# line to upper right
dc.LineTo((RIGHT,TOP))
        
# to lower right
dc.LineTo((RIGHT,BOTTOM))

# to lower left
dc.LineTo((LEFT,BOTTOM))

# to upper left
dc.LineTo((LEFT,TOP))
        
for x in range(LEFT,RIGHT,int(20*mm)):
    for y in range(TOP,BOTTOM,int(20*mm)):
                
        dc.MoveTo((x-CS,y))
        dc.LineTo((x+CS,y))
                
        dc.MoveTo((x,y-CS))
        dc.LineTo((x,y+CS))
                
        dc.TextOut(x,y,"(%d,%d)"%(x,y))

dc.EndPage()
dc.EndDoc()
