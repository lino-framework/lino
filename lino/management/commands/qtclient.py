# -*- coding: UTF-8 -*-
# Copyright 2017-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.core.management.base import BaseCommand
from django.conf import settings


import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QMessageBox, QDesktopWidget, QMainWindow,
                             QAction, qApp, QTextEdit, QHBoxLayout,
                             QVBoxLayout)
# from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from lino.api import rt
from lino.core.menus import Menu  # , MenuItem
from unipath import Path
images_path = Path(settings.STATIC_ROOT, Path('static/images/mjames'))

class ItemCaller(object):
    def __init__(self, win, mi):
        self.mi = mi
        self.win  = win

    def __call__(self, event):
        if False:
            QMessageBox.question(
                self.win, str(self.mi.label),
                str(self.mi.help_text),
                QMessageBox.Yes |
                QMessageBox.No, QMessageBox.Yes)

        self.frm = DetailForm(self.win, self.mi)
        self.frm.show()


class DetailForm(QWidget):

    def __init__(self, win, mi):
        self.mi = mi
        super().__init__(win)
        self.setWindowTitle(str(self.mi.label))
        self.initUI()

    def initUI(self):

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        # self.show()


class LinoClient(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        self.setGeometry(300, 300, 300, 220)
        self.center()
        self.setWindowTitle('qtclient.py')
        self.setWindowIcon(QIcon('../../.static/logo.png'))
        self.setToolTip('This is a <b>QWidget</b> widget')
        self.menubar = self.menuBar()

        user_type = rt.models.users.UserTypes.get_by_value('900')
        menu = settings.SITE.get_site_menu(user_type)
        self.load_menu(menu, self.menubar)
        self.show()
        self.statusBar().showMessage('Ready')

    def load_menu(self, menu, menubar):
        for mi in menu.items:
            if isinstance(mi, Menu):
                submenu = menubar.addMenu(str(mi.label))
                self.load_menu(mi, submenu)
            else:
                a = QAction(QIcon(images_path.child('cancel.png')),
                            str(mi.label), self)
                if mi.hotkey:
                    a.setShortcut(mi.hotkey)
                a.setStatusTip(str(mi.help_text))
                a.triggered.connect(ItemCaller(self, mi))
                menubar.addAction(a)

        # fileMenu = menubar.addMenu('&File')
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.setStatusTip('Exit application')
        # exitAction.triggered.connect(qApp.quit)
        # fileMenu.addAction(exitAction)

        # a = QAction(QIcon('detail.png'), '&Detail', self)
        # a.triggered.connect(self.show_detail)
        # fileMenu.addAction(a)

        # self.toolbar = self.addToolBar('Exit')
        # self.toolbar.addAction(exitAction)

        # btn = QPushButton('Quit', self)
        # btn.clicked.connect(QCoreApplication.instance().quit)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        # btn.resize(btn.sizeHint())
        # btn.move(50, 50)

    # def show_detail(self, event):
    #     self.detail_form = DetailForm()
    #     self.detail_form.show()

    def closeEvent(self, event):

        if True:
            event.accept()
            return

        reply = QMessageBox.question(self, 'MessageBox',
            "This will close the window! Are you sure?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Command(BaseCommand):
    help = """Run a Qt client for this site."""

    def handle(self, *args, **options):

        app = QApplication(sys.argv)
        self.ex = LinoClient()
        # sys.exit(app.exec_())
        return app.exec_()
