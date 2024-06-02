import os
import ctypes
from PySide6.QtGui import QIcon


DB_PATH = os.path.join(".data", "records.db")
UI_FOLDER_PATH = os.path.join("grad_time", "ui")
STYLE_SHEET = "QPushButton:disabled { color: gray; }"


def set_window_icon(window):
    """Sets the window icon and the taskbar icon as well"""
    window.setWindowIcon(QIcon(os.path.join(UI_FOLDER_PATH, "icon.png")))
    myappid = "some.stupid.thig.that.must.be.done"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
