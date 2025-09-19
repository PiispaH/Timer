from time import gmtime, strftime
from PySide6.QtCore import Signal, Slot, QObject
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QCloseEvent, QKeyEvent
from .timer_thread import TimerThread
from .category_dropdown import EditableComboBox
from .database.handle_database import DatabaseHandler
from utils import STYLE_SHEET, set_window_icon
from .category import Category


class MainWindow(QMainWindow):
    """Class for the main window of the application"""

    main_window_clicked = Signal()

    def __init__(self):
        from timer.ui.main_window import Ui_MainWindow

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        set_window_icon(self)
        self._db_handler = DatabaseHandler()
        categories = self._recreate_categories(self._db_handler.get_categories())
        self._category_combobox = EditableComboBox(
            self, self.ui.comboBox_category, categories
        )
        self.setStyleSheet(STYLE_SHEET)
        self.ui.button_stop_timer.setEnabled(False)
        self.ui.button_start_timer.setEnabled(
            self._category_combobox.currentIndex() != -1
        )
        self._elapsed_time = 0.0
        self._timer = TimerThread()
        self._connect_signals()

        self._session_time = 0.0

    def _connect_signals(self):
        """Connects the signals"""
        self.ui.button_start_timer.clicked.connect(self._start_timer)
        self.ui.button_stop_timer.clicked.connect(self._stop_timer)
        self._timer.update_time.connect(self._update_status)
        self._category_combobox.currentIndexChanged.connect(
            self._handle_category_change
        )
        self._category_combobox.new_category_created.connect(
            self._handle_new_category_added
        )

    @Slot(Category)
    def _handle_new_category_added(self, category: Category):
        """Adds the new category to the database"""
        self._set_timer_button_states(False)
        self._db_handler.new_category(category)

    @Slot(int)
    def _handle_category_change(self, index: int):
        """Fetches the data of the selected category from the database and refreshes the
        windows with the new data"""
        if (index != 0 and not index) or index < 0:
            raise IndexError(f"Invalid category index: {index}")
        category = self._category_combobox.current_category
        self.ui.label_6.setText(strftime("%H:%M:%S", gmtime(category.duration)))

    @staticmethod
    def _recreate_categories(categories) -> set[Category]:
        loaded_cats = set()
        for name, data in categories.items():
            loaded_cats.add(Category(data["id"], name, data["duration"]))
        return loaded_cats

    def _start_timer(self):
        """Starts the timer in another thread"""
        self._category_combobox.interactable = False
        self._set_timer_button_states(True)
        self.ui.label_2.setText("00:00:00")
        if not self._timer.isRunning():
            self._timer.start()

    @Slot(float)
    def _update_status(self, elapsed_time: float):
        """Sets the current elapsed time to the window."""
        formatted_time = strftime("%H:%M:%S", gmtime(elapsed_time))
        self.ui.label_2.setText(formatted_time)

    def _stop_timer(self):
        """Stops the timer"""
        self._set_timer_button_states(False)
        self._timer.stop()

        self._session_time += self._timer.elapsed_time()
        formatted_time = strftime("%H:%M:%S", gmtime(self._session_time))
        self.ui.label_4.setText(formatted_time)

        start, end = self._timer.get_data()
        category = self._category_combobox.current_category
        self._db_handler.add_record(category, start, end)
        self._category_combobox.interactable = True

    def _set_timer_button_states(self, timing: bool):
        """Enables the other button and disables the other"""
        self.ui.button_start_timer.setEnabled(not timing)
        self.ui.button_stop_timer.setEnabled(timing)

    def mousePressEvent(self, event: QKeyEvent):
        self.main_window_clicked.emit()
        super().mousePressEvent(event)

    def closeEvent(self, event: QCloseEvent):
        """Handles QCLoseEvents"""
        if self._timer.isRunning():
            self._timer.stop()
            start, end = self._timer.get_data()
            category = self._category_combobox.current_category
            self._db_handler.add_record(category, start, end)
        self._db_handler.close()
        super().closeEvent(event)
