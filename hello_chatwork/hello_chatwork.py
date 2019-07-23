#!/usr/bin/env python
import argparse
import datetime
import inquirer
import json
import re
import requests as req

API_BASE_URL = 'https://api.chatwork.com/v2'

def end_point_url (end_point):
    return "/".join([API_BASE_URL] + end_point.split('_'))

def format_message (message):
    st = datetime.datetime.fromtimestamp(message['send_time'])
    return "[%s %s] %s: %s" % (message['message_id'], st.strftime('%Y/%m/%d %H:%M:%S'), message['account']['name'], re.sub(r'\r?\n', '\n', message['body']))

def main ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--access_token', help="Chatwork Access Token")
    parser.add_argument('-r', '--room_id', help="Chatwork Room ID")
    parser.add_argument('-o', '--output', help="Filename to output")
    args = parser.parse_args()

    if args.access_token is None:
        questions = [
            inquirer.Text('access_token', message="ChatWork Access Token"),
        ]
        ans = inquirer.prompt(questions)
        access_token = ans['access_token']
    else:
        access_token = args.access_token

    headers = {
        'X-ChatWorkToken': access_token,
    }

    if args.room_id is None:
        res = req.get(end_point_url('rooms'), headers=headers)
        if res.status_code != 200:
            raise Exception("HTTP Request Error: status_code=%s" % (res.status_code))
        rooms = json.loads(res.text)
        questions = [
            inquirer.List(
                "room",
                message="Which room's log do you need?",
                choices=list(map(lambda r: "\t".join(map(str, [r['room_id'], r['name']])), rooms)),
                carousel=True,
            )
        ]
        ans = inquirer.prompt(questions)
        room_id = ans['room'].split('\t')[0]
    else:
        room_id = args.room_id

    res = req.get(end_point_url('rooms_%s_messages' % room_id), headers=headers, params={'force': 1})

    if not re.match(r'^2', str(res.status_code)):
        raise Exception("HTTP Request Error: status_code=%s" % (res.status_code));
    messages = json.loads(res.text)

    if args.output is None:
        for message in messages:
            print(format_message(message))
    else:
        with open(args.output, "w") as f:
            for message in messages:
                f.write(format_message(message))
