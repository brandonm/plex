import os
import requests
import json
import sys
import argparse
from argparse import RawTextHelpFormatter


################################ EDIT ###############################

tau_url = 'https://tautulli.domain.ltd'

plex_url = 'https://plex.domain.ltd:32400'

tau_api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

plex_token = 'XXXXXXXXXXXXXXXX'

plex_log_location = '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/'

#################### DO NOT EDIT BELOW THIS LINE ####################

def get_activity(key):
    payload = {'apikey': '{}'.format(tau_api_key), 'cmd': 'get_activity'}
    get_tau_activity = requests.get('{}/api/v2'.format(tau_url), params=payload).json()['response']['data']
    count = get_tau_activity['{}'.format(key)]
    return count

def get_web_threads(type):
    get_plex_threads = requests.get('{}/connections?X-Plex-Token={}'.format(plex_url, plex_token))
    if type == 'count':
        output = len(get_plex_threads.text.split('\n'))
    elif type == 'dump':
        output = (get_plex_threads.text)
    return output

def count_lines(file):
    with open(file) as websoc_log:
        for i, l in enumerate(websoc_log):
            pass
    return i + 1

def web_soc_search(search_string, file):
    with open(file, 'r') as searchfile:
        for line in searchfile:
            if search_string in line:
                print (line)

def log_error_count(file):
    count = 0
    with open(file, 'r') as searchfile:
        for line in searchfile:
            if 'ERROR' in line:
                count = count + 1
        return count

STREAM_SELECTOR = ['total', 'direct_stream', 'direct_play' , 'transcode']

WEBTHREAD_SELECTOR = ['count', 'dump']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Plex helth/stats operations', formatter_class=RawTextHelpFormatter)

    parser.add_argument("--get_stream_count", type=str, choices=STREAM_SELECTOR,
        help='Get stream counts from Tautulli.\nChoices: (%(choices)s)')

    parser.add_argument("--get_web_threads", type=str, choices=WEBTHREAD_SELECTOR,
        help='Get web threads info from the plex server.\nChoices: (%(choices)s)')

    parser.add_argument("--count_lines", action='store_true',
        help='Count lines in the specified file.')

    parser.add_argument("--web_socket_search", type=str,
        help='Search the websocket log file.')

    parser.add_argument("--error_count",  action='store_true',
        help='Count errors present in log file.')

    parser.add_argument("--plex_server_log",  action='store_true',
        help='Use plex server log ie. Plex Media Server.log')

    parser.add_argument("--file", type=str,
        help='Location of a log file')

    opts = parser.parse_args()

    if opts.get_stream_count == 'total':
        print (get_activity('stream_count'))

    elif opts.get_stream_count == 'transcode':
        print (get_activity('stream_count_transcode'))

    elif opts.get_stream_count == 'direct_stream':
        print (get_activity('stream_count_direct_stream'))

    elif opts.get_stream_count == 'direct_play':
        print (get_activity('stream_count_direct_play'))

    elif opts.get_web_threads == 'count':
        print (get_web_threads('count'))

    elif opts.get_web_threads == 'dump':
        print (get_web_threads('dump'))

    elif opts.count_lines:
        if not opts.file:
            print('ERROR: --file argument must be supplied')
        else:
            print (count_lines(opts.file))

    elif opts.web_socket_search:
        if not opts.file:
            print('ERROR: --file argument must be supplied')

        else:
            web_soc_search(opts.web_socket_search, opts.file)

    elif opts.error_count:
        if opts.plex_server_log:
            print (log_error_count('{}Plex Media Server.log'.format(plex_log_location)))

        elif not opts.file:
            print('ERROR: --file argument or --plex_server_log must be supplied')

        else:
            print (log_error_count(opts.file))

    elif len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
