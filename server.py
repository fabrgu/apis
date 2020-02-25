from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'


API_KEY = os.environ['TICKETMASTER_KEY']
BASE_URL = 'https://app.ticketmaster.com/discovery/v2/events'


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', request.args.get('keyword'))
    postalcode = request.args.get('zipcode', request.args.get('zipcode'))
    radius = request.args.get('radius', request.args.get('radius'))
    unit = request.args.get('unit', request.args.get('unit'))
    sort = request.args.get('sort', request.args.get('sort'))

    payload = {'apikey': API_KEY,
               'keyword': keyword,
               'postalCode': postalcode,
               'radius': radius,
               'unit': unit,
               'sort': sort}

    # TODO: Make a request to the Event Search endpoint to search for events
    #
    # - Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results
    res = requests.get(BASE_URL, params=payload)

    data = res.json()
    events = data['_embedded']['events']

    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function
    url = f"{BASE_URL}/{id}"
    payload = {'apikey': API_KEY}
    res = requests.get(url, params=payload)
    data = res.json()

    return render_template('event-details.html', event=data)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
