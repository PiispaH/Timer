import os
import sys
import ctypes
from PySide6.QtGui import QIcon

PLATFORM = "win" if sys.platform == "win32" else "unix"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, ".data", "records.db")
UI_FOLDER_PATH = os.path.join("timer", "ui")

STYLE_SHEET = "QPushButton:disabled { color: gray; }"


def set_window_icon(window):
    """Sets the window icon and the taskbar icon as well"""
    window.setWindowIcon(QIcon(os.path.join(UI_FOLDER_PATH, "icon.png")))
    if PLATFORM == "win":
        myappid = "some.stupid.thing.that.must.be.done"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
