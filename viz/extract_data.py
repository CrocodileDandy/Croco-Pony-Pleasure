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
        if(number in [19021,19031,19011]): #Lets not import everything when testing
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

print data[19011].head()


data[19031].resample('1Min',fill_method='pad')
data[19021].resample('1Min',fill_method='pad')
data[19011].resample('1Min',fill_method='pad')


# data[19011].align(data[19021])

print data[19011].head()
print data[19021].head()


# pouet['bikes'].plot()
# data[19031]['bikes'].plot()
# data[19021]['bikes'].plot()
# data[19011]['bikes'].plot()

plt.show()