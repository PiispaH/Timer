from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QComboBox, QLineEdit
from PySide6.QtCore import Slot, QTimer, Qt


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def closeEvent(self, event):
        self.setText("")
        self.clearFocus()
        super().closeEvent(event)


class EditableComboBox(QComboBox):
    """An editable combobox"""
    def __init__(self, parent, combo_box):
        super().__init__(parent)
        self.setGeometry(combo_box.geometry())
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._categories = self.get_categories()
        self.addItems(self._categories)

    @Slot()
    def add_new_category(self):
        """Adds new items"""
        new_item = self.currentText()
        if new_item and new_item not in self._categories:
            self._categories.add(new_item)
            self.setCurrentIndex(self.count() - 1)
        self.lineEdit().clearFocus()
        self.setEditable(False)

    def get_categories(self) -> set:
        """Gets the categories from storage"""
        categories = set()
        return categories

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape and self.lineEdit():
            self.lineEdit().close()
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """Main method overridden to achieve editing the box with double click"""
        self._timer.start(250)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Main method overridden to achieve editing the box with double click"""
        if self.rect().contains(event.pos()) and self._timer.isActive():
            self._timer.timeout.connect(self.showPopup)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Main method overridden to achieve editing the box with double click"""
        self._timer.timeout.disconnect(self.showPopup)
        self._timer.stop()
        self.setEditable(True)
        self.setLineEdit(CustomLineEdit(self))
        self.lineEdit().setFocus()
        self.lineEdit().selectAll()
        self.parent().main_window_clicked.connect(self.lineEdit().close)
        self.lineEdit().editingFinished.connect(self.add_new_category)
