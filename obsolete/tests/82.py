#coding: latin1
## Copyright 2003-2007 Luc Saffre

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
"""
from lino.misc.tsttools import TestCase, main

class Case(TestCase):
    todo="make keycodes those of wxPython. Or change wxtoolkit.py"
    def test01(self):
        import wx
        s=""
        for name in dir(wx):
            if name.startswith("WXK_"):
                s += "class %s(Hotkey): keycode=%d\n" % (
                    name[4:],getattr(wx,name))

        self.assertEquivalent(s,"""
class ADD(Hotkey): keycode=335
class ALT(Hotkey): keycode=307
class BACK(Hotkey): keycode=8
class CANCEL(Hotkey): keycode=303
class CAPITAL(Hotkey): keycode=311
class CLEAR(Hotkey): keycode=305
class COMMAND(Hotkey): keycode=400
class CONTROL(Hotkey): keycode=308
class DECIMAL(Hotkey): keycode=340
class DELETE(Hotkey): keycode=127
class DIVIDE(Hotkey): keycode=341
class DOWN(Hotkey): keycode=319
class END(Hotkey): keycode=314
class ESCAPE(Hotkey): keycode=27
class EXECUTE(Hotkey): keycode=322
class F1(Hotkey): keycode=342
class F10(Hotkey): keycode=351
class F11(Hotkey): keycode=352
class F12(Hotkey): keycode=353
class F13(Hotkey): keycode=354
class F14(Hotkey): keycode=355
class F15(Hotkey): keycode=356
class F16(Hotkey): keycode=357
class F17(Hotkey): keycode=358
class F18(Hotkey): keycode=359
class F19(Hotkey): keycode=360
class F2(Hotkey): keycode=343
class F20(Hotkey): keycode=361
class F21(Hotkey): keycode=362
class F22(Hotkey): keycode=363
class F23(Hotkey): keycode=364
class F24(Hotkey): keycode=365
class F3(Hotkey): keycode=344
class F4(Hotkey): keycode=345
class F5(Hotkey): keycode=346
class F6(Hotkey): keycode=347
class F7(Hotkey): keycode=348
class F8(Hotkey): keycode=349
class F9(Hotkey): keycode=350
class HELP(Hotkey): keycode=325
class HOME(Hotkey): keycode=315
class INSERT(Hotkey): keycode=324
class LBUTTON(Hotkey): keycode=301
class LEFT(Hotkey): keycode=316
class MBUTTON(Hotkey): keycode=304
class MENU(Hotkey): keycode=309
class MULTIPLY(Hotkey): keycode=336
class NEXT(Hotkey): keycode=313
class NUMLOCK(Hotkey): keycode=366
class NUMPAD0(Hotkey): keycode=326
class NUMPAD1(Hotkey): keycode=327
class NUMPAD2(Hotkey): keycode=328
class NUMPAD3(Hotkey): keycode=329
class NUMPAD4(Hotkey): keycode=330
class NUMPAD5(Hotkey): keycode=331
class NUMPAD6(Hotkey): keycode=332
class NUMPAD7(Hotkey): keycode=333
class NUMPAD8(Hotkey): keycode=334
class NUMPAD9(Hotkey): keycode=335
class NUMPAD_ADD(Hotkey): keycode=392
class NUMPAD_BEGIN(Hotkey): keycode=387
class NUMPAD_DECIMAL(Hotkey): keycode=395
class NUMPAD_DELETE(Hotkey): keycode=389
class NUMPAD_DIVIDE(Hotkey): keycode=396
class NUMPAD_DOWN(Hotkey): keycode=381
class NUMPAD_END(Hotkey): keycode=386
class NUMPAD_ENTER(Hotkey): keycode=372
class NUMPAD_EQUAL(Hotkey): keycode=390
class NUMPAD_F1(Hotkey): keycode=373
class NUMPAD_F2(Hotkey): keycode=374
class NUMPAD_F3(Hotkey): keycode=375
class NUMPAD_F4(Hotkey): keycode=376
class NUMPAD_HOME(Hotkey): keycode=377
class NUMPAD_INSERT(Hotkey): keycode=388
class NUMPAD_LEFT(Hotkey): keycode=378
class NUMPAD_MULTIPLY(Hotkey): keycode=391
class NUMPAD_NEXT(Hotkey): keycode=384
class NUMPAD_PAGEDOWN(Hotkey): keycode=385
class NUMPAD_PAGEUP(Hotkey): keycode=383
class NUMPAD_PRIOR(Hotkey): keycode=382
class NUMPAD_RIGHT(Hotkey): keycode=380
class NUMPAD_SEPARATOR(Hotkey): keycode=393
class NUMPAD_SPACE(Hotkey): keycode=370
class NUMPAD_SUBTRACT(Hotkey): keycode=394
class NUMPAD_TAB(Hotkey): keycode=371
class NUMPAD_UP(Hotkey): keycode=379
class PAGEDOWN(Hotkey): keycode=369
class PAGEUP(Hotkey): keycode=368
class PAUSE(Hotkey): keycode=310
class PRINT(Hotkey): keycode=321
class PRIOR(Hotkey): keycode=312
class RBUTTON(Hotkey): keycode=302
class RETURN(Hotkey): keycode=13
class RIGHT(Hotkey): keycode=318
class SCROLL(Hotkey): keycode=367
class SELECT(Hotkey): keycode=320
class SEPARATOR(Hotkey): keycode=338
class SHIFT(Hotkey): keycode=306
class SNAPSHOT(Hotkey): keycode=323
class SPACE(Hotkey): keycode=32
class SPECIAL1(Hotkey): keycode=193
class SPECIAL10(Hotkey): keycode=202
class SPECIAL11(Hotkey): keycode=203
class SPECIAL12(Hotkey): keycode=204
class SPECIAL13(Hotkey): keycode=205
class SPECIAL14(Hotkey): keycode=206
class SPECIAL15(Hotkey): keycode=207
class SPECIAL16(Hotkey): keycode=208
class SPECIAL17(Hotkey): keycode=209
class SPECIAL18(Hotkey): keycode=210
class SPECIAL19(Hotkey): keycode=211
class SPECIAL2(Hotkey): keycode=194
class SPECIAL20(Hotkey): keycode=212
class SPECIAL3(Hotkey): keycode=195
class SPECIAL4(Hotkey): keycode=196
class SPECIAL5(Hotkey): keycode=197
class SPECIAL6(Hotkey): keycode=198
class SPECIAL7(Hotkey): keycode=199
class SPECIAL8(Hotkey): keycode=200
class SPECIAL9(Hotkey): keycode=201
class START(Hotkey): keycode=300
class SUBTRACT(Hotkey): keycode=339
class TAB(Hotkey): keycode=9
class UP(Hotkey): keycode=317
class WINDOWS_LEFT(Hotkey): keycode=397
class WINDOWS_MENU(Hotkey): keycode=399
class WINDOWS_RIGHT(Hotkey): keycode=398
        """)

                
if __name__ == '__main__':
    main()

