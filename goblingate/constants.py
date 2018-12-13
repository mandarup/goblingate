
import collections


Signal =  collections.namedtuple('Signal', ['ON', 'OFF'])
SIGNAL = Signal(ON=True, OFF=False)


# Speed of sound in cm/s at temperature
TEMPERATURE = 20
SOUND_SPEED = 33100 + (0.6*TEMPERATURE)
