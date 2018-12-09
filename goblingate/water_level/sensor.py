

#!/usr/bin/python
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# |R|a|s|p|b|e|r|r|y|P|i|-|S|p|y|.|c|o|.|u|k|
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# ultrasonic_2.py
# Measure distance using an ultrasonic module
# in a loop.
#
# Ultrasonic related posts:
# http://www.raspberrypi-spy.co.uk/tag/ultrasonic/
#
# Author : Matt Hawkins
# Date   : 16/10/2016
# -----------------------

# -----------------------
# Import required Python libraries
# -----------------------
from __future__ import print_function
import time
import RPi.GPIO as GPIO

from dateutil import relativedelta
import datetime as dt
import numpy as np
import signal


from goblingate.assets import tank
from goblingate.assets import clock
from goblingate.assets import relay

# -----------------------
# Define constants
# -----------------------
# NOTE: make this enum
class Signal(object):
    ON = True
    OFF = False


SIGNAL = Signal()

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
UPDATE_INTERVAL = 5
ULTRASONIC_SENSOR_PULSE_DELAY = .2

# Speed of sound in cm/s at temperature
TEMPERATURE = 20
SOUND_SPEED = 33100 + (0.6 * TEMPERATURE)


def measure(trigger, echo):
    # This function measures a distance
    GPIO.output(trigger, False)
    GPIO.output(trigger, True)
    # Wait 10us
    time.sleep(0.00001)
    GPIO.output(trigger, False)
    # start = time.time()

    # print('echo: {}'.format(GPIO.input(GPIO_ECHO)))
    while GPIO.input(echo)==0:
        start = time.time()

    while GPIO.input(echo)==1:
        stop = time.time()

    # stop = time.time()
    elapsed = stop-start
    distance = (elapsed * SOUND_SPEED)/2.

    return distance


class TimeoutException(Exception):
    """Custom exception class"""
    pass

def timeout_handler(signum, frame):
    """Custom signal handler"""
    raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)


def measure_average(trigger, echo):
    # This function takes 3 measurements and
    # returns the average.

    distance = None
    distances = []
    precision = 2
    i = 0
    start_time = time.time()

    while True:
        signal.alarm(1)
        try:
            print('next measurement...')
            d = measure(trigger, echo)
            print('>>> measure {} : {}'.format(i, d))
            distances.append(d)
            print('pause between measurements for {}s'.format(ULTRASONIC_SENSOR_PULSE_DELAY))
            time.sleep(ULTRASONIC_SENSOR_PULSE_DELAY)
        except TimeoutException:
            print('timeout measurement after 1 s')
            continue # continue the for loop if function A takes more than 5 second
        except Exception as e:
            # raise e
            print(str(e))
            # distances = reject_outliers(distances)
        finally:
            # Reset the alarm
            signal.alarm(0)
        i += 1
        if round(time.time() - start_time,1) >= UPDATE_INTERVAL - 1e-1:
            break

    try:
        #distance = np.mean(distances)
        distance = np.median(distances)
    except Exception as e:
        # warnings.warn(str(e))
        # logging.info(str(e))
        raise e
    print('>>> median measure: {}'.format(d))

    return distance



def relay_logic_upper(upper_relay, upper_tank, lower_tank, clock_times):
    action_time = False
    now = dt.datetime.now().time()
    for t in clock_times:
        if t.start <= now < t.stop:
            action_time = True
            break
        else:
            print("wrong time ", t.start, now, t.stop)
            upper_relay.update(SIGNAL.OFF)

    if action_time:
        if upper_tank.is_high:
            upper_relay.update(SIGNAL.OFF)
            print('detected upper high, setting upper relay OFF')
        elif not upper_tank.is_high and not lower_tank.is_low:
            if not upper_relay.is_on:
                upper_relay.update(SIGNAL.ON)
                print('setting upper relay ON')
            else:
                print('upper relay is already ON')
        else:
            print("No conditions met, setting upper relay OFF")
            upper_relay.update(SIGNAL.OFF)

    if upper_relay.start_time is not None and upper_relay.stop_time is None:
        print(dt.datetime.now(), upper_relay.start_time)
        dur = dt.datetime.now() - upper_relay.start_time
        print('upper relay on dur: {}'.format(dur.total_seconds()))
        if dur.total_seconds() >= UPPER_RELAY_MAX_DUR:
            upper_relay.update(SIGNAL.OFF)
            print('upper relay max dur exceeded, forcing OFF.')
    print('relay state: {}'.format(upper_relay.is_on))
    return upper_relay


def relay_logic_lower(lower_relay, lower_tank, clock_times):
    action_time = False
    now = dt.datetime.now().time()
    for t in clock_times:
        if t.start <= now < t.stop:
            action_time = True
            break
        else:
            print("wrong time ", t.start, now, t.stop)
            lower_relay.update(SIGNAL.OFF)

    if action_time:
        if not lower_tank.is_high:
            if not lower_relay.is_on:
                print('setting lower relay ON {}'.format(lower_relay.is_on))
                lower_relay.update(SIGNAL.ON)
            else:
                print('lower relay is already ON')
        else:
            lower_relay.update(SIGNAL.OFF)
            print('setting lower relay OFF')
    print("lower tank is high: {}".format(lower_tank.is_high))
    print('lower relay state: {}'.format(lower_relay.is_on))

    if lower_relay.start_time is not None and lower_relay.stop_time is None:
        dur = dt.datetime.now() - lower_relay.start_time
        if dur.total_seconds() >= LOWER_RELAY_MAX_DUR:
            lower_relay.update(SIGNAL.OFF)
            print('lower relay max dur exceeded, forcing OFF.')
    return lower_relay


# ----------------------
# test input
# ----------------------

def test_init():
    upper_tank = tank.Tank(low=UPPER_LOW, high=UPPER_HIGH)
    lower_tank = tank.Tank(low=LOWER_LOW, high=LOWER_HIGH)
    upper_tank_relay = relay.Relay(duration=20)
    lower_tank_relay = relay.Relay(duration=20)

    now = dt.datetime.now()
    clock_times_upper = [
        clock.Period(
            now.time(),
            (now +
             relativedelta.relativedelta(
                 seconds=300)).time()),
        clock.Period((now + relativedelta.relativedelta(seconds=620)).time(),
               (now + relativedelta.relativedelta(seconds=700)).time())]
    clock_times_lower = [
        clock.Period(
            (now +
             relativedelta.relativedelta(
                 seconds=300)).time(),
            (now +
             relativedelta.relativedelta(
                 seconds=600)).time()),
        clock.Period((now + relativedelta.relativedelta(seconds=700)).time(),
               (now + relativedelta.relativedelta(seconds=800)).time())]
    print('clock times ', [(c.start, c.stop) for c in clock_times_upper])
    return upper_tank, lower_tank, upper_tank_relay, lower_tank_relay, clock_times_upper, clock_times_lower

# -----------------------
# Main Script
# -----------------------

def main():
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)


    print("Ultrasonic Measurement")
    print("Speed of sound is", SOUND_SPEED / 100, "m/s at ", TEMPERATURE, "deg")

    # Set pins as output and input
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Trigger
    GPIO.setup(GPIO_ECHO, GPIO.IN)      # Echo

    GPIO.setup(GPIO_RELAY_UPPER, GPIO.OUT)
    GPIO.setup(GPIO_RELAY_LOWER, GPIO.OUT)


    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)
    GPIO.output(GPIO_RELAY_UPPER, False)
    GPIO.output(GPIO_RELAY_LOWER, False)


    # Allow module to settle
    time.sleep(0.5)


    # Wrap main content in a try block so we can
    # catch the user pressing CTRL-C and run the
    # GPIO cleanup function. This will also prevent
    # the user seeing lots of unnecessary error
    # messages.
    try:
        # relay = RelayState(dur_keep_on=20)
        upper_tank, lower_tank, upper_tank_relay, lower_tank_relay, clock_times_upper, clock_times_lower = test_init()
        while True:
            print('reading distance...')
            upper_level = measure_average(GPIO_TRIGGER, GPIO_ECHO)
            print("upper tank level : {0:5.1f}".format(upper_level))
            # time.sleep(1)

            # upper_tank = set_tank_state(upper_tank, upper_level)
            print('updating upper tank')
            upper_tank.update(upper_level)
            print(upper_tank.__dict__)

            print('updating lower tank')
            lower_tank.update(8)
            print(lower_tank.__dict__)

            upper_tank_relay = relay_logic_upper(
                upper_tank_relay, upper_tank, lower_tank, clock_times_upper)

            lower_tank_relay = relay_logic_lower(
                lower_tank_relay, lower_tank, clock_times_lower)

            GPIO.output(GPIO_RELAY_UPPER, upper_tank_relay.is_on)
            GPIO.output(GPIO_RELAY_LOWER, lower_tank_relay.is_on)

            if upper_tank_relay.stop_time is not None:
                upper_tank_relay.reset()
            if lower_tank_relay.stop_time is not None:
                lower_tank_relay.reset()

    except KeyboardInterrupt:
        # User pressed CTRL-C
        # Reset GPIO settings
        GPIO.cleanup()


if __name__ == '__main__':
    main()
