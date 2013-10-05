#!/usr/bin/env python
"""
Functions for the velib main program
"""
from matplotlib import pyplot as pl
import json, time, numpy as np

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
    Make the time evolution data of available bikes
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
    return t,vel


def cut_days(t,vel):
    '''
    Cut cumulated avaiable bikes data and sort it by days
    '''
    t_temp = t[:]
    vel_temp = vel[:]
    days_data = {}
    t_day = []
    vel_day = []
    day = time.localtime(t_temp[-1])[2]
    while t_temp != []:
        if time.localtime(t_temp[-1])[2] == day:
            t_day.append(t_temp.pop())
            vel_day.append(vel_temp.pop())
        else:
            days_data[str(time.localtime(t_day[-1])[2])+'/'+str(time.localtime(t_day[-1])[1])+'/'+str(time.localtime(t_day[-1])[0])] = zip(reversed(t_day),reversed(vel_day))
            t_day = []
            vel_day = []
            day = time.localtime(t_temp[-1])[2]
    days_data[str(time.localtime(t_day[-1])[2])+'/'+str(time.localtime(t_day[-1])[1])+'/'+str(time.localtime(t_day[-1])[0])] = zip(reversed(t_day),reversed(vel_day))
    return days_data


def plot_compared_days(days_data,ref_day):
    '''
    Plot available bikes number evolution by days, being compared to a specific day
    '''
    pl.figure()
    for day in days_data.keys():
        first_event = time.localtime(days_data[day][0][0])
        first_time = 3600*first_event[3]+60*first_event[4]+first_event[5]
        days_data[day] = [(ele[0] + first_time - days_data[day][0][0],ele[1]) for ele in days_data[day]]
    ref_data = days_data[ref_day]
    for day in [day for day in days_data.keys() if day!=ref_day]:
        ref = ref_data[:]
        day2process = days_data[day][:]
        day_comp = []
        while ref != [] and day2process != []:
            if ref[0][0] < day2process[0][0]:
                temp = ref.pop(0)
                day_comp.append((day2process[0][0],day2process[0][1]-temp[1]))
            if ref[0][0] > day2process[0][0]:
                temp = day2process.pop(0)
                day_comp.append((ref[0][0],temp[1]-ref[0][1]))
            if day2process[0][0] == ref[0][0]:
                temp1 = ref.pop(0)
                temp2 = day2process.pop(0)
                day_comp.append((temp1[0],temp2[1]-temp1[1]))
        pl.plot([ele[0] for ele in day_comp],[ele[1] for ele in day_comp],label = day)
    pl.legend()
    pl.grid('on')
    pl.title('# of available bikes compared to 15/08/2013')
    pl.xlabel('Time (s)')
    pl.ylabel('# of available bikes')


def plot_bike_time_evol_by_days(days_data):
    pl.figure()
    for day in days_data.keys():
        first_event = time.localtime(days_data[day][0][0])
        first_time = 3600*first_event[3]+60*first_event[4]+first_event[5]
        days_data[day] = [(ele[0] + first_time - days_data[day][0][0],ele[1]) for ele in days_data[day]]
    for day in days_data.keys():
        pl.plot([ele[0] for ele in days_data[day]],[ele[1] for ele in days_data[day]],label = day)
    pl.legend()
    pl.grid('on')
    pl.title('Time evolution of total number of available bikes by days')
    pl.xlabel('Time (s)')
    pl.ylabel('# of available bikes')


def plot_bike_time_evol(t,vel):
    pl.figure()
    pl.plot(t-t[0],vel)
    pl.xlim(0,max(t)-t[0])
    pl.grid('on')
    pl.title('Time evolution of total number of available bikes')
    pl.xlabel('Time (s)')
    pl.ylabel('Total number of bikes')