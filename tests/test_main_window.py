import unittest
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt, QEventLoop, QTimer
from PySide6.QtTest import QTest
from grad_time.main_window import MainWindow


class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not QApplication.instance():
            QApplication()

    def setUp(self):
        self.main_window = MainWindow()
        self.main_window.show()
    
    def tearDown(self):
        self.main_window.closeEvent(QCloseEvent())
        super().tearDown()
    
    def test_window_is_visible(self):
        self.assertTrue(self.main_window.isVisible())

    def test_timer(self):
        """Tests that the timer starts and stops when the buttons are pressed"""
        self.assertFalse(self.main_window.timer.isRunning())
        start_button = self.main_window.ui.button_start_timer
        stop_button = self.main_window.ui.button_stop_timer
        
        QTest.mouseClick(start_button, Qt.LeftButton)

        # Just so that the timer has enough time to start.
        loop = QEventLoop()
        QTimer.singleShot(1, loop.quit)
        loop.exec_()

        self.assertTrue(self.main_window.timer.isRunning())

        QTest.mouseClick(stop_button, Qt.LeftButton)
        self.assertFalse(self.main_window.timer.isRunning())
