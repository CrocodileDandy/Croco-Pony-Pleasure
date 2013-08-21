#!/usr/bin/env python

from matplotlib import pyplot as pl
import numpy as np, velib_lib as velib, os

data_path = 'Second data - 1 week/'
paris = velib.json_local_loader('Paris.json')
station_numbers = [station for station in os.listdir(data_path)]
station_data = dict()
for station in station_numbers:
    station_data[station] = np.loadtxt(data_path+station,dtype = 'int',delimiter = ',')

# Do whatever you want