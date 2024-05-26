# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.button_start_timer = QPushButton(self.centralwidget)
        self.button_start_timer.setObjectName(u"button_start_timer")
        self.button_start_timer.setGeometry(QRect(90, 100, 75, 24))
        self.button_stop_timer = QPushButton(self.centralwidget)
        self.button_stop_timer.setObjectName(u"button_stop_timer")
        self.button_stop_timer.setGeometry(QRect(90, 150, 75, 24))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(330, 90, 101, 21))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(330, 110, 101, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(330, 140, 101, 21))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(330, 160, 101, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 500, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.button_start_timer.setText(QCoreApplication.translate("MainWindow", u"Start timer", None))
        self.button_stop_timer.setText(QCoreApplication.translate("MainWindow", u"Stop timer", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Time elapsed now:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"TIME", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Time recorded:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"TIME", None))
    # retranslateUi

