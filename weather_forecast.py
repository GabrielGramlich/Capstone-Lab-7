'''
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
		'''I imagine I would want to log here, and as
		 CRITICAL, and let the user know the program
		 won't work, so sorry.'''
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
		'''Here I imagine there's not really much point in logging,
		 but maybe it's not an issue of user input, so log it as
		 INFO, maybe? Still let the user know it's an invalid
		 selection, cause then they can try something different.'''
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
