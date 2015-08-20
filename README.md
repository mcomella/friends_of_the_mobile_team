## Pre-requisites
You must have the [requests] module installed:

    pip install requests

[requests]: http://www.python-requests.org/

## Running
To run, add an `emails.txt` file in the same directory you run the
script from that contains one email address per line that you'd
like to not be included in the query. Then:

    ./friends.py

This will print the wiki markup to copy into the page.

More usefully, on OS X:

    ./friends.py | pbcopy

Note that this script assumes it will be run on the day of the meeting because
it generates a parameter that is the date from seven days ago.
