# -*- coding: utf-8 -*-

"""Console script for goblingate."""

import argparse
import os
import time

import goblingate
from goblingate.water_level import water_level_monitoring
from goblingate import settings_parser

def water_level(args):
    print('Starting water level automated monitoring and control')

    settings = settings_parser.parse_settings(os.path.join(args.dir, 'settings.yml'))
    wlsettings = settings_parser.parse_water_level_settings(settings)
    water_level_monitoring.start_monitoring(wlsettings)

def futureplaceholder(args):
    print('Whoopsi-doodle-do')


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

water_level_parser = subparsers.add_parser('water_level')
water_level_parser.add_argument('--dir', type=str, required=True)  # add the name argument
water_level_parser.set_defaults(func=water_level)  # set the default function to hello

goodbye_parser = subparsers.add_parser('futureplaceholder')
goodbye_parser.add_argument('name')
goodbye_parser.set_defaults(func=futureplaceholder)

def main():
    # set timezone
    os.environ['TZ'] = 'Asia/Kolkata'
    time.tzset()

    # invoke cli
    args = parser.parse_args()
    args.func(args)  # call the default function

if __name__ == '__main__':
    main()
