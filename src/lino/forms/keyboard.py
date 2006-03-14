## Copyright 2005-2006 Luc Saffre 

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


class Hotkey:
    keycode=None
    shift=False
    ctrl=False
    alt=False

    def match_wx(self,evt):
        # evt is a wxPython KeyEvent
        print evt
        if evt.GetKeyCode() != self.keycode:
            return False
        if evt.AltDown() != self.alt:
            print evt.AltDown(), self.alt
            return False
        if evt.CtrlDown() != self.ctrl: return False
        if evt.ShiftDown() != self.shift: return False
        return True
            
    
class ESC(Hotkey):
    keycode=27
    
class RET(Hotkey):
    keycode=13

class F1(Hotkey):
    keycode=342
    
