# import library
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# set pandas display
pd.set_option('display.max_rows', 5000)
pd.set_option('display.width', 10000)

# import data from csv
df_activities = pd.read_csv(r"/Users/dermotsheridan/Downloads/UCD/Project /garminproject/2021-10-11_garmin_connect_export/activities.csv")

# Removes any duplicate activities
df_activities.drop_duplicates(subset='Activity ID', inplace=True)

# Data analysis
print(df_activities.shape)
print(df_activities.head())
print(df_activities.info())

# Categories of Name, Location & Type
# Print unique values
print('Activity Name: ', df_activities['Activity Name'].unique(), "\n")
Activity_Name_counts = df_activities['Activity Name'].value_counts(sort=True)
print(Activity_Name_counts)
# Print unique values of
print('Location Name: ', df_activities['Location Name'].unique(), "\n")
Loc_counts = df_activities['Location Name'].value_counts(sort=True)
print(Loc_counts)
# Print unique values
print('Activity Type: ', df_activities['Activity Type'].unique(), "\n")
Act_type_counts = df_activities['Activity Type'].value_counts(sort=True)
print(Act_type_counts)

# Filter activities where activity type is 'Strength training'
st = df_activities[df_activities['Activity Type'] == 'Strength Training']
print(st.head())
print(len(st))

# Clean and Validate

# examine the data types in each column
print(df_activities.dtypes)

# convert columns to correct types
dt_lst = ['Start Time', 'End Time']
# convert columns to date time
for col in dt_lst:
    df_activities[col]= pd.to_datetime(df_activities[col], utc= True)
# Write an assert statement making sure of conversion
    assert df_activities[col].dtype == 'datetime64[ns, UTC]'

hms_lst = ['Duration (h:m:s)', 'Elapsed Duration (h:m:s)', 'Moving Duration (h:m:s)']
for col in hms_lst:
    df_activities[col] = pd.to_timedelta(df_activities[col])
# Write an assert statement making sure of conversion
    assert df_activities[col].dtype == 'timedelta64[ns]'

# Working with Date & Time
# The date of my first and last session
first_session = min(df_activities['Start Time'])
last_session = max(df_activities['Start Time'])

first_session_date = 'My first session date: ' + first_session.strftime('%m/%d/%Y')
last_session_date = 'My last session date: '  + last_session.strftime('%m/%d/%Y')
print(first_session_date)
print(last_session_date)

# total time in days active
total_days_between_sessions = last_session - first_session
print('Total days between first and last session :' + str(total_days_between_sessions.days))

print('Counting the number of session per year')
# No. of session in 2021
session2021 = 0
for s in df_activities['Start Time']:
    if s.year == 2021:
        session2021 = session2021 + 1
print('Number of sessions in 2021: ' + str(session2021))

print('Creating a function for counting session')
# created a function to count session per year
def countsession(year):
    ses = 0
    for s in df_activities['Start Time']:
        if s.year == year:
            ses = ses + 1
    # return ses
    print('Number of sessions in ' + str(year) + " was: " + str(ses))

# count the number of session in each year
countsession(2021)
countsession(2020)
countsession(2019)
countsession(2018)
countsession(2017)
countsession(2016)

# no of session per month over the 5 years
session_per_month = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
for s in df_activities['Start Time']:
    month = s.month
    session_per_month[month] +=1
print('Number of session per month over the 5 years :' + str(session_per_month))

# Training in the morning vs evening
session_count = {'AM': 0, 'PM': 0}
for s in df_activities['Start Time']:
    if s.hour < 12:
        session_count['AM'] += 1
    else:
        session_count['PM'] += 1
print('Number of session Morning and Evening :' +str(session_count))

# Total count
sum_cols = ['Steps','Calories','Elevation Gain (m)',
            'Duration (h:m:s)','Elapsed Duration (h:m:s)',
            'Moving Duration (h:m:s)',
            'Distance (km)']
print('Total Counts during Training History')
print(df_activities[sum_cols].sum())

df_agg_type = df_activities.groupby('Activity Type').size().to_frame('Count')
print('Activity Type')
print(df_agg_type)
df_agg_type = df_agg_type[df_agg_type['Count']>2].sort_values(by='Count')
plt.figure(figsize=(9,9))

cmap = plt.get_cmap('Set2')
colors = [cmap(i) for i in np.linspace(0, 1, 7)]
plt.pie(df_agg_type['Count'],
        labels=df_agg_type.index,
        autopct='%1.0f%%',
        textprops={'fontsize': 14},colors=colors)
plt.show()

sns.barplot(y=df_agg_type.index,x=df_agg_type.Count, orient='h')
plt.show()
