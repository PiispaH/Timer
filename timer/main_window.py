from time import gmtime, strftime
from datetime import datetime
from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QCloseEvent, QKeyEvent
from .timer_thread import TimerThread
from .save_times import write_data
from .category_dropdown import EditableComboBox
from .database.handle_database import DatabaseHandler
from utils import STYLE_SHEET, set_window_icon


class MainWindow(QMainWindow):
    """Class for the main window of the application"""

    main_window_clicked = Signal()

    def __init__(self):
        from timer.ui.main_window import Ui_MainWindow

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        set_window_icon(self)
        self.db_handler = DatabaseHandler()
        self.category_ids = self.db_handler.get_categories()
        self.category_combobox = EditableComboBox(
            self, self.ui.comboBox_category, set(self.category_ids.keys())
        )
        self.setStyleSheet(STYLE_SHEET)
        self.ui.button_stop_timer.setEnabled(False)
        self.elapsed_time = 0.0
        self.timer = TimerThread()
        self.connect_signals()

        self._session_time = 0.0
        self._category_time = 0.0

    def connect_signals(self):
        """Connects the signals"""
        self.ui.button_start_timer.clicked.connect(self.start_timer)
        self.ui.button_stop_timer.clicked.connect(self.stop_timer)
        self.timer.update_time.connect(self._update_status)
        self.category_combobox.currentIndexChanged.connect(self._handle_category_change)
        self.category_combobox.new_category_created.connect(
            self._handle_new_category_added
        )

    @Slot(str)
    def _handle_new_category_added(self, category: str):
        """Adds the new category to the database"""
        category_id = self.db_handler.new_category(category)
        self.category_ids[category] = category_id

    @Slot(int)
    def _handle_category_change(self, index: int):
        """Fetches the data of the selected category from the database and refreshes the
        windows with the new data"""
        # TODO: Some query here to load the data from the DB

    def start_timer(self):
        """Starts the timer in another thread"""
        self.set_timer_button_states(True)
        self.ui.label_2.setText("00:00:00")
        if not self.timer.isRunning():
            self.timer.start()

    @Slot(float)
    def _update_status(self, elapsed_time: float):
        """Sets the current elapsed time to the window."""
        formatted_time = strftime("%H:%M:%S", gmtime(elapsed_time))
        self.ui.label_2.setText(formatted_time)

    def stop_timer(self):
        """Stops the timer"""
        self.set_timer_button_states(False)
        self.timer.stop()

        self._session_time += self.timer.elapsed_time()
        formatted_time = strftime("%H:%M:%S", gmtime(self._session_time))
        self.ui.label_4.setText(formatted_time)

        start, end = self.timer.get_data()
        category = self.category_combobox.current_category()
        self.db_handler.add_record(self.category_ids[category], start, end)

    def set_timer_button_states(self, timing: bool):
        """Enables the other button and disables the other"""
        self.ui.button_start_timer.setEnabled(not timing)
        self.ui.button_stop_timer.setEnabled(timing)

    def mousePressEvent(self, event: QKeyEvent):
        self.main_window_clicked.emit()
        super().mousePressEvent(event)

    def closeEvent(self, event: QCloseEvent):
        """Handles QCLoseEvents"""
        if self.timer.isRunning():
            self.timer.stop()
            start, end = self.timer.get_data()
            category = self.category_combobox.current_category()
            self.db_handler.add_record(self.category_ids[category], start, end)
        self.db_handler.close()
        super().closeEvent(event)
