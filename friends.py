#!/usr/bin/env python2

from datetime import datetime, timedelta
import requests
import urllib

BASE_URL = 'https://bugzilla.mozilla.org/rest/bug'

params = {
    'include_fields': 'id,summary,status,assigned_to',
    'product': [
        'Android Background Services',
        'Firefox for Android',
        'Firefox for iOS',
    ],
    'bug_status': 'RESOLVED',
    'chfield': 'bug_status',
    'chfieldto': 'Now',
    'chfieldvalue': 'RESOLVED',
}

DATE_PARAM = 'chfieldfrom={}'  # YYYY-MM-DD

EMAIL_LINE = 'email{}={}'
EMAIL_NUM_PARAM_LINES = [
    'emailtype{}=notequals',
    'emailassigned_to{}=1',
]

def generate_email_params(address, count):
    out = []
    for line in EMAIL_NUM_PARAM_LINES:
        out.append(line.format(count))
    out.append(EMAIL_LINE.format(count, urllib.quote(address)))
    return out

def generate_date_param():
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    return DATE_PARAM.format(seven_days_ago)

date_param = generate_date_param()
email_params = []
with open('emails.txt', 'r') as f:
    for i, email in enumerate(f, start=1):
        email = email.strip()  # Remove newline
        email_params.extend(generate_email_params(email, i))

params = '&'.join(CONST_PARAMS + [date_param] + email_params)
out = URL + '?' + params
print(out)
