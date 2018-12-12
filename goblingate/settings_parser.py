
import yaml
import copy

def parse_settings(path):
    stg = yaml.safe_load(open(path))
    return stg


def parse_timers(timers):
    parsed = []
    for item in timers:
        t_start = dt.datetime.strptime(item['START'], '%H:%M:%S').time()
        t_stop = dt.datetime.strptime(item['STOP'], '%H:%M:%S').time()
        parsed.append({'START': t_start, 'STOP': t_stop})
    return parsed

def parse_water_level_settings(settings):
    wlsettings = settings['HOME_WATER_SYS']
    parsed = copy.deepcopy(wlsettings)

    parsed['CLOCK_TIMES_UPPER_TANK'] = parse_timers(wlsettings['CLOCK_TIMES_UPPER_TANK'])
    parsed['CLOCK_TIMES_LOWER_TANK'] = parse_timers(wlsettings['CLOCK_TIMES_LOWER_TANK'])

    return parsed
