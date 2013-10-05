from __future__ import division
import pandas as pd
import os 
import csv
from descartes import PolygonPatch
from matplotlib import pylab as plt
import osgeo.ogr
import shapely.wkt
import voronoi_poly


def plot_line(ax,ob):
    x,y=ob.xy
    ax.plot(x,y,color='black',linewidth=1,alpha=0.5)

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

cells=voronoi_poly.VoronoiPolygons(stations_pos, BoundingBox="PARIS", PlotMap=False)



'''
IMPORT PARIS MAP

Plotting the whole map takes A LOT of time... Maybe we should restrict to a few roads? 
Change the shapefile.
'''
shapefile = osgeo.ogr.Open("ile-de-france_highway.shp")
layer = shapefile.GetLayer(0)


# print '\nImport roads in wkt format...'
# roads=[]
# #import the polygons in wkt
# for i in range(layer.GetFeatureCount()):
#     feature = layer.GetFeature(i)
#     geometry = feature.GetGeometryRef()
#     wkt = geometry.ExportToWkt()
#     roads.append(shapely.wkt.loads(wkt))
# print 'Done.'



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


'''
PLOT THE HEAT MAP FOR EVERY DATE
'''
for i,d in enumerate(dates):
	print 'Ploting configuration %s/%s'%(i,len(dates))

	fig=plt.figure()
	ax=plt.subplot(111)

	# Start by plotting the underlying road network
	# for r in roads:
	#     plot_line(ax,r)

	# Now plot the Voronoi cells. Color gives the status of the station
	for c in cells:
	    try:
	        Ndispo=bikes[int(cells[c]['info'])][d]
	        Nslot=slots[int(cells[c]['info'])][d]
	        Ntot=slots[int(cells[c]['info'])][d]+bikes[int(cells[c]['info'])][d]
	        r_vdispo=Nslot/Ntot
	        # Green -> taux=1 & White -> taux=0
	        patch = PolygonPatch(cells[c]['obj_polygon'], fc=plt.get_cmap('Greens')(r_vdispo), ec=plt.get_cmap('Greens')(r_vdispo), alpha=0.8, zorder=1)
	        ax.add_patch(patch)
	    except:
	        patch = PolygonPatch(cells[c]['obj_polygon'], fc='red', ec='#6699cc', alpha=1, zorder=1)
	        ax.add_patch(patch)


	ax.relim()
	ax.autoscale_view(True,True,True)
	frame1=plt.gca()
	frame1.axes.get_xaxis().set_ticks([])
	frame1.axes.get_yaxis().set_ticks([])
	plt.xlabel(r'%s'%d,fontsize=10)
	plt.title(r'$Slot\, availability$',fontsize=25)    
	plt.savefig('test_vid/slots_availability/%03d.png'%i)
	plt.close(fig)