from __future__ import division
import os
from matplotlib import pylab as plt
import csv

'''
IMPORT ACTUAL DATA
'''
data={}
folder='data/2013-07-17/'
list_files=os.listdir(folder)
for f in list_files:
    input=open(folder+f,'rb')
    dump=csv.reader(input,delimiter=" ")

    data[int(f)]=[[],[],[]]
    for rows in dump:
        data[int(f)][0].append(int(rows[0]))
        data[int(f)][1].append(int(rows[1]))
        data[int(f)][2].append(int(rows[2]))
input.close()

dispo=[]
free=[]
for d in data:
    try:
        Ndispo=data[d][2][0]
        Nfree=data[d][1][0]
        Ntot=data[d][2][0]+data[d][1][0]
        r_vdispo=Ndispo#/Ntot
        r_sfree=Nfree#/Ntot

        dispo.append(r_vdispo)
        free.append(r_sfree)
    except:
        pass


dispo=sorted(dispo,reverse=True)
free=sorted(free,reverse=True)

plt.plot([i for i in range(len(dispo))],dispo,'o')
plt.plot([i for i in range(len(free))],free,'o')
plt.yscale('log')
# plt.xscale('log')
plt.show()