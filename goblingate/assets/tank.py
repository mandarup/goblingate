
class Tank(object):
    def __init__(self, high=None, low=None):
        self.is_low = False
        self.is_high = False
        self.is_ok = False

        self.HIGH = high
        self.LOW = low

    def reset(self):
        self.is_ok = False
        self.is_low = False
        self.is_high = False

    def update(self, level):
        if self.LOW <= level:
            self.is_low = True
            self.is_high = False
        elif self.HIGH >= level:
            self.is_low = False
            self.is_high = True
        else:
            self.is_ok = True
            self.is_low = False
            self.is_high = False
        return self

