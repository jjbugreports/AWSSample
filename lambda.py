from __future__ import print_function

import json
import urllib2


def convert_temp(temp_data):
    temp_data['min'] = int(temp_data['min'] * (9/5.0) -459.67)
    temp_data['max'] = int(temp_data['max'] * (9/5.0) -459.67)
    return temp_data

def lambda_handler(event, context):
    # TODO: Key removed from source control. Should be stored in encrypted config.
    key = 'DUMMY'
    try:
        response = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?id=5327684&cnt=10&appid={}'.format(key))
    except Exception as e:
        return {}
    ret_value = {}
    ret_value['list'] = [{'summary': weather_data['weather'][0]['main'], 'description': weather_data['weather'][0]['description'], 'temp': convert_temp(weather_data['temp'])} for weather_data in json.load(response)['list']]
    return ret_value
