#import pandas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta, timezone

#set pandas display
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)

#import data from csv
df_activities = pd.read_csv(r"/Users/dermotsheridan/PycharmProjects/Garmin/garmin-connect-export-master/2021-10-11_garmin_connect_export/activities.csv")

#data analysis
print(df_activities.shape)
print(df_activities.head())
print(df_activities.info())

#removes any duplicate activities
df_activities.drop_duplicates(subset='Activity ID', inplace=True)

# convert columns to correct types
dt_lst = ['Start Time', 'End Time']
#convert colums to date time
for col in dt_lst:
    df_activities[col]= pd.to_datetime(df_activities[col], utc= True)
print('Working with Date & Time')
print('Date & Time :' +  str(df_activities['Start Time'].iloc[1]))
#pick out the year
print('Year :' +  str(df_activities['Start Time'].iloc[1].year))
#pick out the month
print('Month :' +  str(df_activities['Start Time'].iloc[1].month))
##pick out the day
print('Day :' +  str(df_activities['Start Time'].iloc[1].day))
##pick out the hour
print('Hour :' +  str(df_activities['Start Time'].iloc[1].hour))
#pick out the minute
print('Minute :' +  str(df_activities['Start Time'].iloc[1].minute))
#pick out the second
print('Second :' +  str(df_activities['Start Time'].iloc[1].second))
print('Counting the number of session per year')
# No. of session in 2021
session2021 = 0
for s in df_activities['Start Time']:
    if s.year == 2021:
        session2021 = session2021 + 1
print('Number of sessions in 2021: ' + str(session2021))

# No. of session in 2020
session2020 = 0
for s in df_activities['Start Time']:
    if s.year == 2020:
        session2020 = session2020 + 1
print('Number of sessions in 2020: ' + str(session2020))


print('Creating a function for counting session')
#created a function to count session per year
def countsession(year):
    ses = 0
    for s in df_activities['Start Time']:
        if s.year == year:
            ses = ses + 1
    #return ses
    print('Number of sessions in ' + str(year) + " was: " + str(ses))

#count the number of session in each year
countsession(2021)
countsession(2020)
countsession(2019)
countsession(2018)
countsession(2017)
countsession(2016)

print('Training Duration in Days')
#The date of my first and last session
first_session = min(df_activities['Start Time'])
last_session = max(df_activities['Start Time'])

first_session_date = 'My first session date: ' + first_session.strftime('%m/%d/%Y')
last_session_date = 'My last session date: '  + last_session.strftime('%m/%d/%Y')
print(first_session_date)
print(last_session_date)

#total time in days active
total_days_between_sessions = last_session - first_session
print('Total days between first and last session :' + str(total_days_between_sessions.days))

#no of session per month over the 5 years
session_per_month = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
for s in df_activities['Start Time']:
    month = s.month
    session_per_month[month] +=1
print('Number of session per month over the 5 years :' + str(session_per_month))