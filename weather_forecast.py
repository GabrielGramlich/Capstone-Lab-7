'''
Use the forecast API to create a detailed, neatly formatted 5-day forecast, for anywhere the user chooses. Ask the user for the location.

Make sure your API key is not coded into your program. Your program should read the key from an environment variable. 

Use a query parameter dictionary in the request.

Your forecast should show the temperature and unit (your choice of F or C), weather description, and wind speed for every three hour interval, over the next 5 days.

Your program should handle errors. What type of errors do you anticipate? How will you deal with them?
'''

import requests
import os
from datetime import datetime
import time
import sys

KEY=os.environ.get('WEATHER_KEY')


class WeatherError(Exception):
	pass


def main():
	if KEY is not None:
		location = get_location()
		data = get_weather_data(location)
		items = parse_data(data)
		display_weather_information(items)
	else:
		raise WeatherError('API Key is missing')


def get_location():
	city = input('Which city would you like the forecast for? ')
	country = input('And which country? ')
	return f'{city},{country}'


def get_weather_data(location):
	query = {'q': location, 'units': 'imperial', 'appid': KEY}
	url = 'http://api.openweathermap.org/data/2.5/forecast'
	data = requests.get(url,params=query).json()

	return data


def parse_data(forecast_items):
	try:
		items = []
		for forecast in forecast_items['list']:
			timestamp = forecast['dt']
			'''Using Unix time, because I'm displaying it to the user, not
			 storing it somewhere, or performing some calculation off of it.'''
			date = datetime.fromtimestamp(timestamp)
			temp = round(forecast['main']['temp'],1)
			items.append([date, temp])

		return items
	except KeyError:
		raise WeatherError('Invalid selection.')



def display_weather_information(items):
	for item in items:
		delayed_print(f'at {item[0]}, the temperature is {item[1]}F')


def delayed_print(string):
	'''Couldn't remember how to do this, got the code from here:
	https://stackoverflow.com/questions/4627033/printing-a-string-with-a-little-delay-between-the-chars'''
	for character in string:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.01)
	print()


if __name__ == '__main__':
	main()
