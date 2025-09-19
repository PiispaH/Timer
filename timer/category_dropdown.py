from typing import Any
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import QComboBox, QLineEdit, QMenu, QMessageBox
from PySide6.QtCore import Signal, Slot, QTimer, Qt, QEvent, QObject, QPoint
from .category import Category, CategoryManager


class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def closeEvent(self, event):
        self.setText("")
        self.clearFocus()
        super().closeEvent(event)


class EditableComboBox(QComboBox):
    """An editable combobox"""

    new_category_created = Signal(Category)
    category_removed = Signal(str)

    def __init__(self, parent: Any, combo_box: QComboBox, cat_mngr: CategoryManager):
        super().__init__(parent)
        self.setGeometry(combo_box.geometry())
        self._view = self.view()
        self._view.viewport().installEventFilter(self)
        self._view.setContextMenuPolicy(Qt.CustomContextMenu)
        self._view.customContextMenuRequested.connect(self.context_menu_for_list)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._cat_mngr = cat_mngr
        for category in cat_mngr.categories:
            self.addItem(category.name, userData=category)
        self.setInsertPolicy(QComboBox.NoInsert)

    @property
    def interactable(self) -> bool:
        return self._interactable

    @interactable.setter
    def interactable(self, state: bool):
        self._interactable = state
        self.setEnabled(state)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """Event filter that allows the popup to stay open when an item is right clicked"""
        if event.type() == QEvent.MouseButtonRelease:
            if QMouseEvent(event).button() == Qt.RightButton:
                return True
        return False

    @Slot(QPoint)
    def context_menu_for_list(self, position: QPoint):
        index = self._view.indexAt(position)
        if not index.isValid():
            return
        item = self.model().data(index, Qt.DisplayRole)
        menu = QMenu()
        menu.addAction("Delete", lambda: self.remove_category(item))
        menu.addAction("Rename", lambda: self.rename_category(item))
        menu.exec(self._view.mapToGlobal(position))

    @property
    def current_category(self) -> Category:
        return self.itemData(self.currentIndex())

    @Slot()
    def add_new_category(self):
        """Adds new items"""
        text = self.currentText()
        if not text:
            self.setEditable(False)
            return
        self.lineEdit().clearFocus()
        cat = self._cat_mngr.new_unique(text)
        self.addItem(cat.name, userData=cat)
        self.setCurrentIndex(self.count() - 1)
        self.new_category_created.emit(cat)
        self.setEditable(False)

    def remove_category(self, category: str):
        """Asks if the user is serious and then removes the category and all associated data"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Confirmation")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setText(f"Are you sure you want to delete <b>{category}</b>?")
        msg_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        result = msg_box.exec()
        if result != QMessageBox.StandardButton.Yes:
            return
        # TODO: actual removal of the data

    def rename_category(self, category):
        """Opens up a dialog where the new name for a category can be entered"""
        # TODO

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape and self.lineEdit():
            self.lineEdit().close()
        super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """Main method overridden to achieve editing the box with double click"""
        if event.buttons() & Qt.LeftButton:
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
