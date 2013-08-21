#!/usr/bin/env python
"""
Functions for the velib main program
"""

import json,urllib, os, numpy as np
from matplotlib import pyplot as pl


def json_local_loader(file_path):
    '''
    A simple json loader for a local file. Strings in Unicode format !
    '''
    return json.loads(next(open(file_path)))


def fetch_statinfo(station,url,key):
    '''
    Fetch the information of a station and append it to a data list.
    Fetch the following information :
    - Rounded epoch time of last update
    - Available bike stands
    - Available bikes
    '''
    opener =  urllib.FancyURLopener()
    fet = json.loads(opener.open(url+str(station)+key).read())
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


def station_data_saver(station,data):
    '''
    A function to save data of a station.
    Checks if the right leaf directory exists, create it if not, compare data and save only if fresher.
    '''
    absolute_path_to_data_folder = '/home/clement/Documents/ProgPython/Homemade/Velib/data/'
    if data == None:
        return
    try:
        station_file = np.loadtxt(absolute_path_to_data_folder+str(station),delimiter = ',',dtype = 'int')
        old_data = station_file.ravel()[-3]
    except IOError:
        create_dir(absolute_path_to_data_folder)
    station_file = open(absolute_path_to_data_folder+str(station),'a')
    try:
        if old_data == data[0]:
            return
        else:
            station_file.write('{0},{1},{2}'.format(str(data[0]),str(data[1]),str(data[2]))+'\n')
    except NameError:
        station_file.write('{0},{1},{2}'.format(str(data[0]),str(data[1]),str(data[2]))+'\n')

        
def mk_interval_hist(station_numbers,station_data):
    intervals = dict()
    for station in station_numbers:
        try:
            intervals[station] = station_data[station][1:,0]-station_data[station][:-1,0]
        except IndexError:
            print('Index problem with station '+station+'. Maybe only one movement')
    intervals_hist = []
    for station in intervals.keys():
        intervals_hist.extend(list(intervals[station]))
    pl.figure(1)
    pl.hist(intervals_hist, bins = 100, normed = True)
    pl.title('Time interval between two movements in a given station')
    pl.xlabel('Time (s)')
    pl.xlim(0,1000)
    pl.figure(2)
    pl.plot(intervals_hist,'+')
    pl.show()


def mk_bike_time_evol(station_numbers,station_data):
    '''
    Make the time evolution graph of available bikes
    '''
    t_init = max([array.ravel()[0] for array in station_data.values()])
    vel_init = sum([array.ravel()[2] for array in station_data.values()])
    evol = []
    for station in station_data.keys():
        try:
            temp = station_data[station][:,0::2]
            temp[1:,1] = temp[1:,1] - temp[:-1,1]
            evol.extend(list(temp[1:,:]))
        except IndexError:
            pass
    evol.sort(key = lambda array: array[0])
    t = [t_init]
    vel = [vel_init]
    for step in evol:
        if step[0] != t[-1]:
            vel.append(vel[-1]+step[1])
            t.append(step[0])
        else:
            vel[-1] = (vel[-1]+step[1])
    pl.plot(t-t_init,vel)
    pl.xlim(0,max(t)-t_init)
    pl.grid('on')
    pl.title('Time evolution of total number of available bikes')
    pl.xlabel('Time (s)')
    pl.ylabel('Total number of bikes')
    pl.show()