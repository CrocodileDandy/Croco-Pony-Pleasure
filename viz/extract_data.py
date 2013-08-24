import pandas as pd
import os 
from matplotlib import pylab as plt

'''
IMPORT ACTUAL DATA
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
        pass



l=0
index=0
for n in data:
	if len(data[n])>l:
		index=n
		l=len(data[n])

data[19031].resample('1Min',fill_method='pad')
print data[19031].describe()

data[19021].resample('1Min',fill_method='pad')
print data[19021].describe()

data[19031]['bikes'].plot()
data[19021]['bikes'].plot()
plt.show()