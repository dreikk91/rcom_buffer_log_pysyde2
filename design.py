# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledHPfylz.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtWidgets import *


class Ui_Rcom_buffer(object):
    def setupUi(self, Rcom_buffer):
        if not Rcom_buffer.objectName():
            Rcom_buffer.setObjectName(u"Rcom_buffer")
        Rcom_buffer.resize(499, 396)
        self.actionSave_to_txt = QAction(Rcom_buffer)
        self.actionSave_to_txt.setObjectName(u"actionSave_to_txt")
        self.actionSave_to_html = QAction(Rcom_buffer)
        self.actionSave_to_html.setObjectName(u"actionSave_to_html")
        self.actionExit_2 = QAction(Rcom_buffer)
        self.actionExit_2.setObjectName(u"actionExit_2")
        self.actionSave_to_markdown = QAction(Rcom_buffer)
        self.actionSave_to_markdown.setObjectName(u"actionSave_to_markdown")
        self.centralwidget = QWidget(Rcom_buffer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)
        self.progressBar.setInvertedAppearance(False)

        self.gridLayout.addWidget(self.progressBar, 4, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 3, 0, 1, 2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout.addWidget(self.pushButton, 4, 1, 1, 1)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setAcceptRichText(False)

        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 2)

        Rcom_buffer.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Rcom_buffer)
        self.statusbar.setObjectName(u"statusbar")
        Rcom_buffer.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(Rcom_buffer)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 499, 21))
        self.menuExit = QMenu(self.menuBar)
        self.menuExit.setObjectName(u"menuExit")
        self.menuExit_2 = QMenu(self.menuBar)
        self.menuExit_2.setObjectName(u"menuExit_2")
        Rcom_buffer.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuExit.menuAction())
        self.menuBar.addAction(self.menuExit_2.menuAction())
        self.menuExit.addAction(self.actionSave_to_txt)
        self.menuExit.addSeparator()
        self.menuExit.addAction(self.actionSave_to_html)
        self.menuExit.addSeparator()
        self.menuExit.addAction(self.actionSave_to_markdown)
        self.menuExit_2.addAction(self.actionExit_2)

        self.retranslateUi(Rcom_buffer)

        QMetaObject.connectSlotsByName(Rcom_buffer)

    # setupUi

    def retranslateUi(self, Rcom_buffer):
        Rcom_buffer.setWindowTitle(QCoreApplication.translate("Rcom_buffer", u"Rcom_buffer", None))
        self.actionSave_to_txt.setText(QCoreApplication.translate("Rcom_buffer", u"Save to text", None))
        # if QT_CONFIG(shortcut)
        self.actionSave_to_txt.setShortcut(QCoreApplication.translate("Rcom_buffer", u"Ctrl+S", None))
        # endif // QT_CONFIG(shortcut)
        self.actionSave_to_html.setText(QCoreApplication.translate("Rcom_buffer", u"Save to html", None))
        # if QT_CONFIG(shortcut)
        self.actionSave_to_html.setShortcut(QCoreApplication.translate("Rcom_buffer", u"Ctrl+H", None))
        # endif // QT_CONFIG(shortcut)
        self.actionExit_2.setText(QCoreApplication.translate("Rcom_buffer", u"Exit", None))
        # if QT_CONFIG(shortcut)
        self.actionExit_2.setShortcut(QCoreApplication.translate("Rcom_buffer", u"Ctrl+E", None))
        # endif // QT_CONFIG(shortcut)
        self.actionSave_to_markdown.setText(QCoreApplication.translate("Rcom_buffer", u"Save to markdown", None))
        self.label.setText(QCoreApplication.translate("Rcom_buffer", u"Buffer size", None))
        self.label_2.setText(QCoreApplication.translate("Rcom_buffer", u"0/5000", None))
        self.pushButton.setText(QCoreApplication.translate("Rcom_buffer", u"Read buffer", None))
        self.menuExit.setTitle(QCoreApplication.translate("Rcom_buffer", u"Options", None))
        self.menuExit_2.setTitle(QCoreApplication.translate("Rcom_buffer", u"Exit", None))
    # retranslateUi
