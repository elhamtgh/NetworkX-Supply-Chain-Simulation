# Simplest way to get the lat, long of any address.

# Using Python requests and the Google Maps Geocoding API.

import requests

GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

params = {'address': 'oshiwara industerial center goregaon west mumbai','sensor': 'false','region': 'india'}

# Do the request and get the response data
req = requests.get(GOOGLE_MAPS_API_URL, params=params)
res = req.json()

# Use the first result
result = res['results'][:]

geodata = dict()
geodata['lat'] = result['geometry']['location']['lat']
geodata['lng'] = result['geometry']['location']['lng']
geodata['address'] = result['formatted_address']

print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))