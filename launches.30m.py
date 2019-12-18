#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>Upcoming Launches</bitbar.title>
# <bitbar.version>v0.0.1</bitbar.version>
# <bitbar.author>Drew Siedel</bitbar.author>
# <bitbar.author.github>dtsiedel</bitbar.author.github>
# <bitbar.desc>Display Upcoming Rocket Launches</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

from requests import get
from datetime import datetime

url = 'https://launchlibrary.net/1.4/launch/next/3'

def separator():
    print('---')

def flag(country_code):
    res = ''
    if country_code == 'USA':
        res += '🇺🇸'
    elif country_code == 'ITA':
        res += '🇮🇹'
    elif country_code == 'CHN':
        res += '🇨🇳'
    elif country_code == 'RUS':
        res += '🇷🇺'
    elif country_code == 'JPN':
        res += '🇯🇵'
    elif country_code == 'IND':
        res += '🇮🇳'
    else:
        res += '❓'

    return res

def rocket():
    print('🚀')

def title():
    rocket()

def gather_data(a_url):
    return get(url).json()

def launch_text(launch):
    video = '(🎥)'
    if len(get_link(launch)) <= 0:
        video = ''
    flag_text = flag(launch.get('lsp').get('countryCode'))
    return '{} {} {}'.format(flag_text, launch['name'].replace('|', '-'), video)

def get_link(launch):
    key = 'vidURLs'
    if len(launch['vidURLs']) > 0:
        return 'href={}'.format(launch['vidURLs'][0])
    return ''

def location_text(launch):
    location = launch.get('location')
    flag_text = flag(location.get('countryCode'))

    return '{} {}'.format(flag_text, location.get('pads')[0].get('name'))

def window_text(launch):
    clock = '🕒'
    start = datetime.fromtimestamp(launch.get('wsstamp'))
    end = datetime.fromtimestamp(launch.get('westamp'))

    return '{} {} - {}'.format(clock, start, end)

def print_data(json_data):
    launches = json_data['launches']
    title()
    for l in launches:
        separator()
        text = launch_text(l)
        color_black = 'color=black'
        link = get_link(l)
        launch_description = '{} | {} {}'.format(text, color_black, link)
        print(launch_description)

        location_description = '      {} | {}'.format(location_text(l), 'trim=false')
        print(location_description)

        window_description = '      {} | {}'.format(window_text(l), 'trim=false')
        print(window_description)
    separator()

def fail():
    print("☠ ")

try:
    print_data(gather_data(url))
except Exception as e:
    fail()
    raise
