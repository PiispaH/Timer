from time import gmtime, strftime
from PySide6.QtCore import Signal, Slot, QSettings
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QCloseEvent, QKeyEvent
from .timer_thread import TimerThread
from .database.handle_database import DatabaseHandler
from utils import STYLE_SHEET, set_window_icon
from .category import Category


class MainWindow(QMainWindow):
    """Class for the main window of the application"""

    main_window_clicked = Signal()

    def __init__(self):
        from timer.ui.main_window import Ui_MainWindow

        super().__init__()
        self._settings = QSettings("PiispaH", "timer", self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Timer")
        set_window_icon(self)
        self.restoreGeometry(self._settings.value("geometry"))
        self.restoreState(self._settings.value("state"))

        self._db_handler = DatabaseHandler()
        self._category_mngr = self._db_handler.get_categories()
        self._category_combobox = (
            self.ui.comboBox_category
        )  # Has already been promoted to EditableComboBox in ui files
        self._category_combobox.setup(self, self._category_mngr)
        self.setStyleSheet(STYLE_SHEET)
        self.ui.button_stop_timer.setEnabled(False)
        self.ui.button_start_timer.setEnabled(
            bool(self._category_combobox.current_category)
        )
        self._elapsed_time = 0.0
        self._timer_thread = TimerThread()
        self._connect_signals()

        self._session_time = 0.0

        # Try to return the last category selection
        if self._category_combobox.current_category:
            last_index = int(self._settings.value("cat_box/selected_index", 0))
            if last_index:
                self._category_combobox.setCurrentIndex(last_index)
            self._update_status(0)

    def _connect_signals(self):
        """Connects the signals"""
        self.ui.button_start_timer.clicked.connect(self._start_timer)
        self.ui.button_stop_timer.clicked.connect(self._stop_timer)
        self._timer_thread.update_time.connect(self._update_status)
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

    def _start_timer(self):
        """Starts the timer in another thread"""
        self._category_combobox.interactable = False
        self._set_timer_button_states(True)
        self.ui.label_2.setText("00:00:00")
        if not self._timer_thread.isRunning():
            self._timer_thread.start()

    @Slot(float)
    def _update_status(self, elapsed_time: float):
        """Updates the times on the counters."""
        self.ui.label_2.setText(strftime("%H:%M:%S", gmtime(elapsed_time)))

        self.ui.label_4.setText(
            strftime("%H:%M:%S", gmtime(self._session_time + elapsed_time))
        )

        category = self._category_combobox.current_category
        self.ui.label_6.setText(
            strftime("%H:%M:%S", gmtime(category.duration + elapsed_time))
        )

    def _stop_timer(self):
        """Stops the timer and saves the time"""
        self._set_timer_button_states(False)
        self._timer_thread.stop()
        dur = self._timer_thread.duration

        self._session_time += dur

        start, end = self._timer_thread.get_data()
        category = self._category_combobox.current_category
        category.duration += dur
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
        # Save the window geometry and category selections.
        self._settings.setValue("geometry", self.saveGeometry())
        self._settings.setValue("state", self.saveState())
        self._settings.setValue(
            "cat_box/selected_index", self._category_combobox.currentIndex()
        )

        if self._timer_thread.isRunning():
            self._timer_thread.stop()
            start, end = self._timer_thread.get_data()
            category = self._category_combobox.current_category
            self._db_handler.add_record(category, start, end)
        self._db_handler.close()
        super().closeEvent(event)
