from __future__ import division
import pandas as pd
import csv
import os
import osgeo.ogr
import shapely.wkt
import numpy as np
from matplotlib import pylab as plt
from math import sqrt
import pyproj


'''
IMPORT STATIC DATA
'''
input=open('stations.csv','rb')
dump=csv.reader(input,delimiter=",")
proj = pyproj.Proj(proj='utm', zone=31, ellps='clrk66')

stations_pos={}
for i,rows in enumerate(dump):
    if(i>0):
        stations_pos[int(rows[0])]=proj(float(rows[4]),float(rows[3]))
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

d = dates[2]

spatial_correlations = {}

for s1 in bikes:
    spatial_correlations[s1] = []
    x1 = stations_pos[s1][0]
    y1 = stations_pos[s1][1]
    for s2 in bikes: 
        try:
            x2 = stations_pos[s2][0]
            y2 = stations_pos[s2][1]
            spatial_correlations[s1].append([bikes[s1][d]*bikes[s2][d],sqrt((x1-x2)**2 + (y1-y2)**2)])
        except:
            pass




distance = []
product = []
for s in spatial_correlations:
    for v in spatial_correlations[s]:
        distance.append(v[1])
        product.append(v[0])




distance,product = zip(*sorted(zip(distance,product),reverse=1))

Nbins = 100
bins = np.linspace(0,20000,Nbins)
digitized = np.digitize(distance, bins)

x_stack=[[] for i in range(Nbins+1)]
y_stack=[[] for i in range(Nbins+1)]

for i,x,y in zip(digitized,distance,product):
    x_stack[i].append(x)
    y_stack[i].append(y)

distance_means=[np.mean(x) for x in x_stack]
product_means=[np.mean(y) for y in y_stack]



plt.plot(distance_means,product_means,'o')
plt.show()