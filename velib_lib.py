#!/usr/bin/env python
"""
Functions for the velib main program
"""
from matplotlib import pyplot as pl
import json

def json_local_loader(file_path):
    '''
    A simple json loader for a local file. Strings in Unicode format !
    '''
    return json.loads(next(open(file_path)))
        
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
