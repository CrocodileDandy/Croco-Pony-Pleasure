#!/usr/bin/env python

import velib_lib as velib

url = 'https://api.jcdecaux.com/vls/v1/stations/'
key = '?contract=Paris&apiKey=3c394c34b27ab10bc764a04395b2c2a417a8ff10'
paris = velib.json_local_loader('/home/clement/Documents/ProgPython/Homemade/Velib//Paris.json')

station_numbers = [paris[i]['number'] for i in range(len(paris))]
for station in station_numbers:
    data = velib.fetch_statinfo(station,url,key)
    velib.station_data_saver(station,data)