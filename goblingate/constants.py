
import collections


Signal =  collections.namedtuple('Signal', ['ON', 'OFF'])
SIGNAL = Signal(ON=True, OFF=False)

# Define GPIO to use on Pi
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO_RELAY_UPPER = 22
GPIO_RELAY_LOWER = 27


UPPER_LOW = 20
UPPER_HIGH = 5  # 20

LOWER_LOW = 20  # 800
LOWER_HIGH = 5  # 20

UPPER_RELAY_MAX_DUR = 10
LOWER_RELAY_MAX_DUR = 100

# N_SAMPLES_PER_INTERVAL = 10
UPDATE_INTERVAL = 5 # update measurement every n seconds
ULTRASONIC_SENSOR_PULSE_DELAY = .2 # seconds

# Speed of sound in cm/s at temperature
TEMPERATURE = 20
SOUND_SPEED = 33100 + (0.6*TEMPERATURE)
