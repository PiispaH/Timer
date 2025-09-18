from time import time
from math import ceil, floor
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
        self._stop_date = None

    def run(self):
        self._start_time = time()
        self._start_date = datetime.now()
        self._running = True
        while self._running:
            # Check ten times in a second if the count has stopped
            for _ in range(10):
                if not self._running:
                    break
                self.msleep(100)
            self.update_time.emit(self.elapsed_time())

    def elapsed_time(self):
        return time() - self._start_time

    def stop(self):
        self._running = False
        self._stop_date = datetime.now()
        self.wait()

    def get_data(self):
        return self._start_date, self._stop_date
