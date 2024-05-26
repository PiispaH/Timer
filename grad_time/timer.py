from time import time
from PySide6.QtCore import QThread, Signal


class TimerThread(QThread):
    "Runs a thread where a timer is running"
    update_time = Signal(int)

    def __init__(self):
        super().__init__()
        self._running = True
        self.start_time = None
        self.elapsed_time = 0

    def run(self):
        self.start_time = time()
        self._running = True
        while self._running:
            self.update_time.emit(self.elapsed_time + time() - self.start_time)
            self.msleep(1000)  # Sleep for 1 second
        self.elapsed_time += round(time() - self.start_time - 1)

    def stop(self):
        self._running = False
        self.wait()
