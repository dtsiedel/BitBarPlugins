#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# -*- coding: utf-8 -*-

# <bitbar.title>Upcoming Launches</bitbar.title>
# <bitbar.version>v0.0.1</bitbar.version>
# <bitbar.author>Drew Siedel</bitbar.author>
# <bitbar.author.github>dtsiedel</bitbar.author.github>
# <bitbar.desc>Display Upcoming Rocket Launches</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>

from requests import get
from datetime import datetime

date_format_string = '%B %d, %Y %H:%M:%S UTC'
url = 'https://launchlibrary.net/1.4/launch/next/5'

flags = {
    'USA': '🇺🇸',
    'ITA': '🇮🇹',
    'CHN': '🇨🇳',
    'RUS': '🇷🇺',
    'JPN': '🇯🇵',
    'IND': '🇮🇳',
    'FRA': '🇫🇷',
    'GUF': '🇬🇫',
    'NZL': '🇳🇿'
}

def separator():
    print('---')

def flag(country_code):
    if country_code in flags:
        return flags[country_code]
    else:
        return '❓'

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

def build_diff_string(diff, time_approx):
    res = ''

    days, seconds = diff.days, diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    if days > 0:
        singular = days == 1
        res += '{} day{}, '.format(days, '' if singular else 's')

    if not time_approx and hours > 0:
        singular = hours == 1
        res += '{} hour{}, '.format(hours, '' if singular else 's')

    if not time_approx and minutes > 0:
        singular = minutes == 1
        res += '{} minute{}, '.format(minutes, '' if singular else 's')

    # strip last comma if we had any entries
    if len(res) > 1:
        res = res[:-2]
    else:
        return "Launch window open!"

    return '{} from now'.format(res)

def window_text(launch):
    clock = '🕒'

    start = datetime.strptime(launch.get('windowstart'), date_format_string)
    diff = start - datetime.utcnow()

    time_approx = start.hour == 0 and start.minute == 0
    diff_string = build_diff_string(diff, time_approx)

    return '{} {}'.format(clock, diff_string)

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
