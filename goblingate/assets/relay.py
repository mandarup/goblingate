
import datetime as dt
import pytz

class RelayStateError(Exception):
    pass


class Relay(object):
    def __init__(self, duration=0):
        self.is_on = False
        self.start_time = None
        self.stop_time = None
        self._duration = duration
        self.history = []
        self.signal = True # True is Normally Open (i.e. switch OFF)

    def reset(self):
        self.is_on = False
        self.start_time = None
        self.stop_time = None
        self.history = []
        self.signal = True

    def update(self, signal):
        if self.is_on and signal:
            raise RelayStateError("Relay is already ON, Received signal ON")
        self.is_on = signal
        if self.is_on:
            self.start_time = dt.datetime.now()
            self.signal = False
        else:
            self.stop_time = dt.datetime.now()
            self.signal = True
        return self
