import _thread as threading
from time import time, sleep


class Countdown:
    """
    Class that tracks a countdown and runs a function on completion
    """
    def __init__(self, on_end, *, hr=0, mins=0, sec=0):
        self.counting
        self.sec = (hr * 60 + mins) * 60 + sec
        self.on_end = on_end

    def start(self):
        threading.start_new_thread(self._start, ())

    def _start(self):
        last = time()

        while self.sec > 0:
            cur = time()
            dt = last-cur
            self.sec -= dt
            last = cur
            sleep(0.05)