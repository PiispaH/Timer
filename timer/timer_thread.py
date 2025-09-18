from time import time
from math import floor
from datetime import datetime
from PySide6.QtCore import QThread, Signal


class TimerThread(QThread):
    "Runs a thread where a timer is running"

    update_time = Signal(float)

    def __init__(self):
        super().__init__()
        self._running = True
        self._start_time = None
        self._start_date = None
        self._stop_time = None
        self._stop_time = None

    def run(self):
        self._start_time = time()
        self._start_date = datetime.now()
        self._running = True
        while self._running:
            self.update_time.emit(self.elapsed_time())
            self.msleep(1000)  # Sleep for 1 second

    def elapsed_time(self):
        return time() - self._start_time

    def stop(self):
        self._running = False
        self._stop_time = time()
        self._stop_date = datetime.now()
        print(time() - self._start_time)
        self.wait()

    def get_data(self):
        return self._start_date, self._stop_date
