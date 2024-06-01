import sys
from PySide6 import QtWidgets
from grad_time.main_window import MainWindow


def main():
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    return app.exec()


if __name__ == "__main__":
    return_code = main()
    sys.exit(return_code)
