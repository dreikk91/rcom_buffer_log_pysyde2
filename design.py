# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitledsiKvoZ.ui'
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
        self.actionExit = QAction(Rcom_buffer)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSave_to_markdown = QAction(Rcom_buffer)
        self.actionSave_to_markdown.setObjectName(u"actionSave_to_markdown")
        self.actionClear_log = QAction(Rcom_buffer)
        self.actionClear_log.setObjectName(u"actionClear_log")
        self.actionRemove_polls_from_buffer = QAction(Rcom_buffer)
        self.actionRemove_polls_from_buffer.setObjectName(u"actionRemove_polls_from_buffer")
        self.centralwidget = QWidget(Rcom_buffer)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setCheckable(False)
        self.pushButton.setChecked(False)
        self.pushButton.setFlat(False)

        self.gridLayout.addWidget(self.pushButton, 9, 1, 1, 1)

        self.progressBar_2 = QProgressBar(self.centralwidget)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setValue(0)

        self.gridLayout.addWidget(self.progressBar_2, 9, 0, 1, 1)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 1, 1, 1)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setAcceptRichText(False)

        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 2)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        Rcom_buffer.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Rcom_buffer)
        self.statusbar.setObjectName(u"statusbar")
        Rcom_buffer.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(Rcom_buffer)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 499, 21))
        self.File = QMenu(self.menuBar)
        self.File.setObjectName(u"File")
        self.menuExit = QMenu(self.menuBar)
        self.menuExit.setObjectName(u"menuExit")
        self.menuOptions = QMenu(self.menuBar)
        self.menuOptions.setObjectName(u"menuOptions")
        Rcom_buffer.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.File.menuAction())
        self.menuBar.addAction(self.menuOptions.menuAction())
        self.menuBar.addAction(self.menuExit.menuAction())
        self.File.addAction(self.actionSave_to_txt)
        self.File.addAction(self.actionSave_to_html)
        self.File.addAction(self.actionSave_to_markdown)
        self.menuExit.addAction(self.actionExit)
        self.menuOptions.addAction(self.actionClear_log)
        self.menuOptions.addAction(self.actionRemove_polls_from_buffer)

        self.retranslateUi(Rcom_buffer)

        QMetaObject.connectSlotsByName(Rcom_buffer)
    # setupUi

    def retranslateUi(self, Rcom_buffer):
        Rcom_buffer.setWindowTitle(QCoreApplication.translate("Rcom_buffer", u"Rcom buffer log", None))
        self.actionSave_to_txt.setText(QCoreApplication.translate("Rcom_buffer", u"Save as csv", None))
#if QT_CONFIG(shortcut)
        self.actionSave_to_txt.setShortcut(QCoreApplication.translate("Rcom_buffer", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_to_html.setText(QCoreApplication.translate("Rcom_buffer", u"Save as html", None))
#if QT_CONFIG(shortcut)
        self.actionSave_to_html.setShortcut(QCoreApplication.translate("Rcom_buffer", u"Ctrl+H", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("Rcom_buffer", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("Rcom_buffer", u"Ctrl+E", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_to_markdown.setText(QCoreApplication.translate("Rcom_buffer", u"Save as markdown", None))
#if QT_CONFIG(shortcut)
        self.actionSave_to_markdown.setShortcut(QCoreApplication.translate("Rcom_buffer", u"Ctrl+M", None))
#endif // QT_CONFIG(shortcut)
        self.actionClear_log.setText(QCoreApplication.translate("Rcom_buffer", u"Clear log", None))
        self.actionRemove_polls_from_buffer.setText(QCoreApplication.translate("Rcom_buffer", u"Remove polls from buffer", None))
        self.pushButton.setText(QCoreApplication.translate("Rcom_buffer", u"Read buffer", None))
        self.label_4.setText(QCoreApplication.translate("Rcom_buffer", u"0/0", None))
        self.label_3.setText(QCoreApplication.translate("Rcom_buffer", u"Rcom buffer size", None))
        self.File.setTitle(QCoreApplication.translate("Rcom_buffer", u"File", None))
        self.menuExit.setTitle(QCoreApplication.translate("Rcom_buffer", u"Exit", None))
        self.menuOptions.setTitle(QCoreApplication.translate("Rcom_buffer", u"Options", None))
    # retranslateUi

