from __future__ import division
import csv
import os
import osgeo.ogr
import shapely.wkt
from matplotlib import pylab as plt
from descartes import PolygonPatch
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
IMPORT ACTUAL DATA
'''
data={}
folder='../data/'
list_files=os.listdir(folder)
lengths=[]
for f in list_files:
    try:
        print folder+f
        input=open(folder+f,'rb')
        dump=csv.reader(input,delimiter=",")

        number=int(f.replace('.csv',''))
        data[number]=[[],[],[]]
        i=0
        for rows in dump:
            data[number][0].append(int(rows[0]))
            data[number][1].append(int(rows[1]))
            data[number][2].append(int(rows[2]))
            i+=1
        lengths.append(i)
        input.close()
    except:
        pass

print min(lengths)



'''
IMPORT PARIS MAP

Plotting the whole map takes A LOT of time... Maybe we should restrict to a few roads? 
Change the shapefile.
'''
shapefile = osgeo.ogr.Open("ile-de-france_highway.shp")
layer = shapefile.GetLayer(0)


print '\nImport roads in wkt format...'
roads=[]
#import the polygons in wkt
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = feature.GetGeometryRef()
    wkt = geometry.ExportToWkt()
    roads.append(shapely.wkt.loads(wkt))
print 'Done.'



'''
PLOT EVERYTHING

'''
plt.figure()
ax=plt.subplot(111)

# Start by plotting the underlying road network
for r in roads:
    plot_line(ax,r)

# Now plot the Voronoi cells. Color gives the status of the station
for c in cells:
    try:
        Ndispo=data[cells[c]['info']][2][5]
        Nfree=data[cells[c]['info']][1][5]
        Ntot=data[cells[c]['info']][2][5]+data[cells[c]['info']][1][5]
        r_vdispo=Ndispo/Ntot
        r_sfree=Nfree/Ntot
    
        tau=r_vdispo
        # Green -> taux=1 & White -> taux=0
        patch = PolygonPatch(cells[c]['obj_polygon'], fc=plt.get_cmap('Greens')(tau), ec=plt.get_cmap('Greens')(tau), alpha=0.8, zorder=1)
        ax.add_patch(patch)
    except:
        patch = PolygonPatch(cells[c]['obj_polygon'], fc='red', ec='#6699cc', alpha=1, zorder=1)
        ax.add_patch(patch)


ax.relim()
ax.autoscale_view(True,True,True)
frame1=plt.gca()
frame1.axes.get_xaxis().set_ticks([])
frame1.axes.get_yaxis().set_ticks([])
plt.show()