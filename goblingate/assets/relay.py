
import datetime as dt

class RelayStateError(Exception):
    pass


class Relay(object):
    def __init__(self, duration=0):
        self.is_on = False
        self.start_time = None
        self.stop_time = None
        self._duration = duration
        self.history = []

    def reset(self):
        self.is_on = False
        self.start_time = None
        self.stop_time = None
        self.history = []

    def update(self, signal):
        if self.is_on and signal:
            raise RelayStateError("Relay is already ON, Received signal ON")
        self.is_on = signal
        if self.is_on:
            self.start_time = dt.datetime.now()
        else:
            self.stop_time = dt.datetime.now()
        return self
