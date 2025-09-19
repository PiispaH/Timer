# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QStatusBar,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_start_timer = QPushButton(self.centralwidget)
        self.button_start_timer.setObjectName("button_start_timer")
        self.button_start_timer.setGeometry(QRect(10, 60, 75, 24))
        self.button_stop_timer = QPushButton(self.centralwidget)
        self.button_stop_timer.setObjectName("button_stop_timer")
        self.button_stop_timer.setGeometry(QRect(10, 100, 75, 24))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(260, 10, 231, 21))
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(260, 30, 101, 16))
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.label_3.setGeometry(QRect(260, 60, 231, 21))
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.label_4.setGeometry(QRect(260, 80, 101, 16))
        self.comboBox_category = QComboBox(self.centralwidget)
        self.comboBox_category.setObjectName("comboBox_category")
        self.comboBox_category.setGeometry(QRect(10, 20, 151, 22))
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.label_5.setGeometry(QRect(260, 110, 231, 21))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.label_6.setGeometry(QRect(260, 130, 101, 16))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 500, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.button_start_timer.setText(
            QCoreApplication.translate("MainWindow", "Start timer", None)
        )
        self.button_stop_timer.setText(
            QCoreApplication.translate("MainWindow", "Stop timer", None)
        )
        self.label.setText(
            QCoreApplication.translate("MainWindow", "Time elapsed now:", None)
        )
        self.label_2.setText(QCoreApplication.translate("MainWindow", "00:00:00", None))
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", "Time recorded in session:", None)
        )
        self.label_4.setText(QCoreApplication.translate("MainWindow", "00:00:00", None))
        self.label_5.setText(
            QCoreApplication.translate("MainWindow", "Time recorded overall:", None)
        )
        self.label_6.setText(QCoreApplication.translate("MainWindow", "00:00:00", None))

    # retranslateUi
