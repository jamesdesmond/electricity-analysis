import numpy as np
import pandas as pd
from mbglob.MbGlob import MbGlob as glob
import re

#Grabs all csv filenames in the Data folder, as a relative path
filepaths = glob().glob("Data/*.csv")
#Dataframe that will hold csv entries
data = pd.DataFrame(columns=['locationName','date','MWhAvg','BizMWhAvg'])
for filepath in filepaths:
    current = pd.read_csv(filepath)
    #Gets just the filename from the filepath
    filename = re.search("[A-Za-z\ ]+[0-9]{6}",filepath).group(0)
    #Getting LocationName and Date from the csv filename
    tuple = str(filename).rpartition(" ")
    locationName = tuple[0]
    date = pd.to_datetime(tuple[2], format='%Y%m',errors='coerce')
    #Calculating MWhAvg
    MWhAvg = current['usage(kWh)'].sum() / 1000
    #Calculating Business Hour Average by adding a day of week column to the temp dataframe
    current['date'] = pd.to_datetime(current['date'])
    current['day_of_week'] = current['date'].dt.dayofweek
    current['day_of_week'] = pd.to_numeric(current['day_of_week'])
    #Calculating Business Day Average by counting business days in the currently parsed month
    count = current[current['day_of_week'] < 5.].count()['day_of_week']
    sum = current[current['day_of_week'] < 5].sum()['usage(kWh)'] / 1000
    BizMWhAvg = sum / count
    tempdf = pd.DataFrame([[locationName,date,MWhAvg,BizMWhAvg]],columns=['locationName','date','MWhAvg','BizMWhAvg'])
    data = data.append(tempdf,ignore_index=True)
#the DataFrame 'data' now holds all the information needed to analyze

#uniqueLocations is a list of all unique locationnames in data
uniqueLocations = data['locationName'].unique()

for uniqueLocation in uniqueLocations:
    #Gets only the rows pertaining to uniqueLocation, then assigns the last row (most recent) to totalUsage
    currentRow = data[data['locationName'] == uniqueLocation].tail(1)
    #Holds the second to most recent row
    oldRow = data[data['locationName'] == uniqueLocation].tail(2).head(1)
    date = currentRow['date'].iat[0].date().strftime('%Y-%m')
    #Total Usage
    print("Electricity Usage Report for " + uniqueLocation + " " + date +" :")
    totalUsage = currentRow['MWhAvg']
    totalUsage = round(float(totalUsage.values),2)
    print("Total Electricity Usage : ")
    print(str(totalUsage) + " MWh")
    #Average Business Day Usage
    bizUsage = currentRow['BizMWhAvg']
    bizUsage = round(float(bizUsage.values),2)
    print("Average Business Day Electricity Usage : ")
    print(str(bizUsage) + " MWh")
    #Month to Month Change to Business Day Usage
    oldBizUsage = oldRow['BizMWhAvg']
    oldBizUsage = round(float(oldBizUsage.values),2)
    #Formula = (currMonth - prevMonth) / prevMonth * 100
    #change is a percentage
    change = round(((bizUsage - oldBizUsage) / oldBizUsage * 100),2)
    change = str(change) + " %"
    print("Month to Month Change to Average Business Day Usage")
    print(change)
    print('********************')