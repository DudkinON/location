import httplib2
import json
from flask import Flask, render_template as render, request

METHODS = ['GET', 'POST']

app = Flask(__name__)


@app.route('/', methods=METHODS)
@app.route('/maps', methods=METHODS)
def maps():
    # google query url
    g_url = 'http://maps.googleapis.com/maps/api/geocode/json?' \
            'sensor=false&address={}'
    # output data
    location = ''
    city_data = ''
    country_data = ''
    if request.method == 'POST':
        # create list of city and country
        city = request.form['city'].split(' ')
        country = request.form['country'].split(' ')
        query_city = ''
        query_country = ''
        # generate query string of city and country
        if len(city) > 1:
            for word in city:
                query_city += query_city + word + '+'
            query_city = query_city.rstrip('+')
        else:
            query_city += city[0]
        if len(country) > 1:
            for word in country:
                query_country += query_country + word + '+'
            query_country = query_country.rstrip('+')
        else:
            query_country += country[0]
        # create url string for query
        url = g_url.format(query_city + '+' + query_country)
        # send request and get response from Google Maps
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        # decode response to string
        result = result.decode("utf-8")
        # create dictionary with response data
        data = json.loads(result)['results'][0]
        # get dictionary with location data
        location = data['geometry']['location']
        # get city long name
        city_data = data['address_components'][0]['long_name']
        # get country long name
        country_data = data['address_components'][3]['long_name']

    return render('maps/data.html', location=location,
                  city=city_data, country=country_data)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
