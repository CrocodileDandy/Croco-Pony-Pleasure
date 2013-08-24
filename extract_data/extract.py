#!/usr/bin/env python
import numpy as np
import json
import urllib
import os

def json_local_loader(file_path):
    '''
    A simple json loader for a local file. Strings in Unicode format !
    '''
    try: 
    	data = json.loads(next(open(file_path)))
    except:
    	return 'The station infos are not in the indicated directory!'

    return data

def fetch_statinfo(station,url,key):
    '''
    Fetch the information of a station and append it to a data list.
    Fetch the following information :
    - Rounded epoch time of last update
    - Available bike stands
    - Available bikes
    '''
    opener =  urllib.FancyURLopener()
    fet = json.loads(opener.open(url+str(station)+'?contract=Paris&apiKey='+str(key)).read())
    try:
        data = (fet['last_update']/1000,fet['available_bike_stands'],fet['available_bikes'])
    except KeyError:
        print('KeyError during attempt to fetch station '+str(station))
    else:
        print(str(station)+' Done')
        return data
        

def create_dir(path):
    '''
    Just create a dir and manage OSError
    '''
    try:
        os.makedirs(path)
    except OSError:
        pass


def station_data_saver(station,data,data_dir):
    '''
    A function to save data of a station.
    Checks if the right leaf directory exists, create it if not, compare data and save only if fresher.
    '''

    if data == None:
        return
    try:
        station_file = np.loadtxt(data_dir+str(station)+'.csv',delimiter = ',',dtype = 'int')
        old_data = station_file.ravel()[-3]
    except IOError:
        create_dir(data_dir)
    station_file = open(data_dir+str(station),'a')
    try:
        if old_data == data[0]:
            return
        else:
            station_file.write('{0},{1},{2}'.format(str(data[0]),str(data[1]),str(data[2]))+'\n')
    except NameError:
        station_file.write('{0},{1},{2}'.format(str(data[0]),str(data[1]),str(data[2]))+'\n')



'''
WHERE THE MAGIC HAPPENS
'''

data_dir=''
stations_file=''

url = 'https://api.jcdecaux.com/vls/v1/stations/'
key = '' #Insert your api key here
paris = json_local_loader(stations_file)

print paris

station_numbers = [paris[i]['number'] for i in range(len(paris))]
for station in station_numbers:
    data = fetch_statinfo(station,url,key)
    station_data_saver(station,data,data_dir)
