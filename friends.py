#!/usr/bin/env python2

from datetime import datetime, timedelta
import requests

import pprint

BASE_URL = 'https://bugzilla.mozilla.org/rest/bug'

params = {
    'include_fields': [
        'assigned_to',
        'id',
        'summary'
    ],
    'product': [
        'Android Background Services',
        'Firefox for Android',
        'Firefox for iOS',
    ],
    'bug_status': 'RESOLVED',
    'chfield': 'bug_status',
    'chfieldto': 'Now',
    # TODO: Only fixed?
    'chfieldvalue': 'RESOLVED',
}


def generate_email_param(address, count):
    count_str = str(count)

    type_key = 'emailtype' + count_str
    email_assigned_key = 'emailassigned_to' + count_str
    email_key = 'email' + count_str

    return {
        type_key: 'notequals',
        email_assigned_key: '1',
        email_key: address,
    }


def generate_from_date_param(days_ago):
    'Returns the date seven days ago in the YYYY-MM-DD format.'
    date_str = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    return {'chfieldfrom': date_str}


def convert_to_wiki_markup(json):
    json = json['bugs']

    output = []
    for bug in json:
        name = bug['assigned_to_detail']['real_name']
        line = '*' + name + ' fixed {{bug|' + str(bug['id']) + '}}'
        line += ' - ' + bug['summary']
        output += [line]
        output.sort()
    return '\n'.join(output)

params.update(generate_from_date_param(7))
with open('emails.txt', 'r') as f:
    for i, email in enumerate(f, start=1):
        email = email.strip()  # Remove newline
        params.update(generate_email_param(email, i))

result = requests.get(BASE_URL, params=params)
markup = convert_to_wiki_markup(result.json())

# Some characters received may cause an exception so encode:
#   http://stackoverflow.com/a/492711
print markup.encode('utf-8')
