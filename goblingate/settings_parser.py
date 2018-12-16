
import yaml
import copy
import os
import datetime as dt
from easydict import EasyDict as edict


class SettingsParserError(Exception):
    pass


def parse_settings(path):
    if not os.path.exists(path):
        raise SettingsParserError('settings file not found at {}'.format(path))
    stg = yaml.safe_load(open(path))
    return edict(stg)


def parse_timers(timers):
    parsed = []
    for item in timers:
        print(item)
        t_start = dt.datetime.strptime(item['START'], '%H:%M').time()
        t_stop = dt.datetime.strptime(item['STOP'], '%H:%M').time()
        parsed.append({'START': t_start, 'STOP': t_stop})
    return parsed


def parse_water_level_settings(settings):
    wlsettings = settings['HOME_WATER_SYS']
    parsed = copy.deepcopy(wlsettings)

    parsed['CLOCK_TIMES_UPPER_TANK'] = parse_timers(wlsettings['CLOCK_TIMES_UPPER_TANK'])
    parsed['CLOCK_TIMES_LOWER_TANK'] = parse_timers(wlsettings['CLOCK_TIMES_LOWER_TANK'])
    parsed['CLOCK_TIMES_GARDEN'] = parse_timers(wlsettings['CLOCK_TIMES_GARDEN'])
    return parsed
