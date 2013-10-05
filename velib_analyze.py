#!/usr/bin/env python

import numpy as np, velib_lib as velib, os
from matplotlib import pyplot as pl

data_path = 'data/Second data - 1 week/'
paris = velib.json_local_loader('Paris.json')
station_numbers = [station for station in os.listdir(data_path)]
station_data = dict()
for station in station_numbers:
    station_data[station] = np.loadtxt(data_path+station,dtype = 'int',delimiter = ',')

# Do whatever you want
t,vel = velib.mk_bike_time_evol(station_numbers,station_data)
days_data = velib.cut_days(t[:],vel[:])
velib.plot_bike_time_evol(t,vel)
#velib.plot_compared_days(days_data,'15/8/2013')
velib.plot_bike_time_evol_by_days(days_data)
pl.show()