from __future__ import division
import pandas as pd
import csv
import os
import osgeo.ogr
import shapely.wkt
import numpy as np
from matplotlib import pylab as plt



'''
IMPORT STATIC DATA
'''
input=open('stations.csv','rb')
dump=csv.reader(input,delimiter=",")

stations_pos={}
for i,rows in enumerate(dump):
    if(i>0):
        stations_pos[int(rows[0])]=(float(rows[4]),float(rows[3]))
input.close()



'''
IMPORT DATA AND RESAMPLE

Looks for the '.csv' files in the ../data folder, takes the name as the station number
Data are loaded in a pandas dataframe, the epoch time is used as an index, and then transformed in TimeStamp (UTC:Paris time) for readability
'''
data={}
folder='../data/'
list_files=os.listdir(folder)
for f in list_files:
    try:
        number = int(f.replace('.csv',''))
        s=pd.read_csv(folder+f,names=['date','slots','bikes'],parse_dates = {'Timestamp' : ['date']}, index_col = 'Timestamp')
        s.index=pd.to_datetime(s.index,unit='s').tz_localize('UTC').tz_convert('Europe/Paris')
        data[number]=s
    except:
        print 'Impossible to read file %s'%f


# Resamples the data to have XX minutes between each timestamp, and extract the number of bikes doing so
bikes={}
slots={}
for station_id in data:
	bikes[station_id] = data[station_id].bikes.resample('15Min',fill_method='pad')
	slots[station_id] = data[station_id].slots.resample('15Min',fill_method='pad')


dates=[]
for date,val in bikes[19031].iteritems():
	dates.append(date)

correlations_bike = {}

d0 = dates[0]
for station_id in data:
	for d in dates[1:]:
		try:
			if (station_id not in correlations_bike):
				correlations_bike[station_id] = []

			correlations_bike[station_id].append(bikes[station_id][d] - bikes[station_id][d0])
		except:
			pass

average = []
for i,d in enumerate(dates):
	average.append([])
	for station_id in correlations_bike:
		try:
			average[-1].append(correlations_bike[station_id][i])
		except:
			pass

average = [np.mean(a) for a in average]

plt.plot([r for r in range(len(average))],average)
plt.show()