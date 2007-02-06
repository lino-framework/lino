## Copyright 2007 Luc Saffre 

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""

This module defines the constants to be used as parameter to
PyCDC.GetDeviceCaps() or win32ui.GetDeviceCaps().  It is a collection
of snippets from different sources. I wrote it just because I didn't
find some of those constants in the win32con package.

http://msdn.microsoft.com/library/default.asp?url=/library/en-us/gdi/devcons_88s3.asp

http://www.dotnet4all.com/Dot-Net-Books/2005/01/how-to-get-same-value-for.html



PHYSICALWIDTH


For printing devices: the width of the physical page, in device
units. For example, a printer set to print at 600 dpi on 8.5-x11-inch
paper has a physical width value of 5100 device units. Note that the
physical page is almost always greater than the printable area of the
page, and never smaller.

PHYSICALHEIGHT

For printing devices: the height of the physical page, in device
units. For example, a printer set to print at 600 dpi on
8.5-by-11-inch paper has a physical height value of 6600 device
units. Note that the physical page is almost always greater than the
printable area of the page, and never smaller. 


PHYSICALOFFSETX

For printing devices: the distance from the left edge of the physical
page to the left edge of the printable area, in device units. For
example, a printer set to print at 600 dpi on 8.5-by-11-inch paper,
that cannot print on the leftmost 0.25-inch of paper, has a horizontal
physical offset of 150 device units.


PHYSICALOFFSETY

For printing devices: the distance from the top edge of the physical
page to the top edge of the printable area, in device units. For
example, a printer set to print at 600 dpi on 8.5-by-11-inch paper,
that cannot print on the topmost 0.5-inch of paper, has a vertical
physical offset of 300 device units.


HORZRES

Width, in pixels, of the screen; or for printers, the width, in
pixels, of the printable area of the page.

VERTRES

Height, in raster lines, of the screen; or for printers, the height,
in pixels, of the printable area of the page.

LOGPIXELSX

Number of pixels per logical inch along the screen width. In a system
with multiple display monitors, this value is the same for all
monitors.

LOGPIXELSY

Number of pixels per logical inch along the screen height. In a system
with multiple display monitors, this value is the same for all
monitors.



"""


# most constants also defined in win32con

DRIVERVERSION  = 0     # 'Device driver version
TECHNOLOGY     = 2     # 'Device classification
HORZSIZE       = 4     # 'Horizontal size in millimeters
VERTSIZE       = 6     # 'Vertical size in millimeters
HORZRES        = 8     # 'Horizontal width in pixels
VERTRES        = 10    #'Vertical height in pixels
BITSPIXEL      = 12    #'Number of bits per pixel
PLANES         = 14    #'Number of planes
NUMBRUSHES     = 16    #'Number of brushes the device has
NUMPENS        = 18    #'Number of pens the device has
NUMMARKERS     = 20    #'Number of markers the device has
NUMFONTS       = 22    #'Number of fonts the device has
NUMCOLORS      = 24    #'Number of colors the device supports
PDEVICESIZE    = 26    #'Size required for device descriptor
CURVECAPS      = 28    #'Curve capabilities
LINECAPS       = 30    #'Line capabilities
POLYGONALCAPS  = 32    #'Polygonal capabilities
TEXTCAPS       = 34    #'Text capabilities
CLIPCAPS       = 36    #'Clipping capabilities
RASTERCAPS     = 38    #'Bitblt capabilities
ASPECTX        = 40    #'Length of the X leg
ASPECTY        = 42    #'Length of the Y leg
ASPECTXY       = 44    #'Length of the hypotenuse
SHADEBLENDCAPS = 45    #'Shading and blending caps (IE5)
LOGPIXELSX     = 88    #'Logical pixels/inch in X
LOGPIXELSY     = 90    #'Logical pixels/inch in Y
SIZEPALETTE    = 104   #'Number of entries in physical palette
NUMRESERVED    = 106   #'Number of reserved entries in palette
COLORRES       = 108   #'Actual color resolution


# the following constants are missing in win32con:

PHYSICALWIDTH   = 110
PHYSICALHEIGHT  = 111
PHYSICALOFFSETX = 112
PHYSICALOFFSETY = 113            
VREFRESH        = 116   #'Current vertical refresh rate of the
                        #'display device (for displays only) in Hz
DESKTOPVERTRES  = 117   #'Horizontal width of entire desktop in pixels (NT5)
DESKTOPHORZRES  = 118   #'Vertical height of entire desktop in pixels (NT5)
BLTALIGNMENT    = 119   #'Preferred blt alignment




