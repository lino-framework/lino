#!/usr/bin/python

import sys
import time
from PyQt4 import QtGui, QtCore

class TrayIcon:
    
    def __init__(self,mainWindow):

        text2=time.strftime("%d") # day of the month as a decimal number (01...31)
        text1=time.strftime("%a").upper()[0:2] # abbreviated weekday name


        #fontName="MS Dialog"
        fontName="Lucida Console"
        #fontName="Terminal"
        fontWeight=QtGui.QFont.Bold

        iconSize=128 # 256
        fontSize=int(iconSize/2.9)
        padding=(iconSize-2*fontSize) / 2

        pixmap=QtGui.QPixmap(iconSize,iconSize)

        painter=QtGui.QPainter(pixmap)
        painter.setPen(QtCore.Qt.yellow)
        painter.setFont(QtGui.QFont(fontName, fontSize, fontWeight))
        painter.drawText(padding,padding+fontSize, text2)

        painter.setFont(QtGui.QFont(fontName, fontSize, fontWeight))
        painter.drawText(padding,(padding+fontSize)*2, text1)
        painter.end()
        
        icon=QtGui.QIcon(pixmap)
        self.ctrl=QtGui.QSystemTrayIcon(icon)
        
        self.iconMenu=QtGui.QMenu()
        self.iconMenu.addAction("&Close TrayDay",mainWindow.close)
        
        self.ctrl.setContextMenu(self.iconMenu)
        self.ctrl.show()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("TrayDay")
        self.trayIcon=TrayIcon(self)

    def close(self):
        self.trayIcon.ctrl.hide()
        QtGui.QMainWindow.close(self)

        
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        sys.exit(-1)

    mainWindow=MainWindow()
    # note that we don't show the main window
    sys.exit(app.exec_())
