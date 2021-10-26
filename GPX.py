# import library
import gpxpy
import gpxpy.gpx
import glob
import os
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 10000)

PATH = 'gpxfolder location'
# create a path to all gpx files
gpx_files = glob.glob(os.path.join(PATH,"*.gpx"))
gpx = gpxpy.parse(open(gpx_files[100]))
print(gpx)

# Track Summary
gpx_track = gpx.tracks[0]
gpx_track
print("Name: " + gpx_track.name)
print("Description: " + str(gpx_track.description))
print("Start: " + str(gpx_track.get_time_bounds().start_time.isoformat()))
print("End: " + str(gpx_track.get_time_bounds().end_time))

bounds = gpx_track.get_bounds()
print("Latitude Bounds: (%f, %f)" % (bounds.min_latitude, bounds.max_latitude))
print("Longitude Bounds: (%f, %f)" % (bounds.min_longitude, bounds.max_longitude))

# Run Duration
# Duration returned in seconds
print('Run Duration in sec :' + str(gpx_track.get_duration()*1./60))

# Run Distance What wat the length of the run?
# Length returned in meters. 2d and 3d distance is available.

# Length returned in meters. 2d .
print('Run Distance 2d:' + str(gpx_track.length_2d()))

# Length returned in meters. 3d
print('Run Distance 3d:' + str(gpx_track.length_3d()))

# Quick Visualisation
track_coords = [[point.latitude, point.longitude, point.elevation]
                for track in gpx.tracks
                for segment in track.segments
                for point in segment.points]

coords_df = pd.DataFrame(track_coords, columns=['Latitude', 'Longitude', 'Altitude'])

fig = plt.figure(figsize=(12, 9))
coords_df.plot('Longitude', 'Latitude', color='#A00084', linewidth=1.5)
plt.show()

# multiple gpx files
from glob import glob

# Multiple GPX files - define a function to read them all at once
def load_gpx_data(gpx_path, filter=""):
    # List all of the GPX files in the path
    gpx_files = glob(os.path.join(gpx_path, filter + "*.gpx"))
    gpx_data = []
    # Loop through the files
    for file_idx, gpx_file in enumerate(gpx_files):
        gpx = gpxpy.parse(open(gpx_file, 'r'))
        # Loop through tracks
        for track_idx, track in enumerate(gpx.tracks):
            track_name = track.name
            track_time = track.get_time_bounds().start_time
            track_length = track.length_3d()
            track_duration = track.get_duration()
            track_speed = track.get_moving_data().max_speed

            for seg_idx, segment in enumerate(track.segments):
                segment_length = segment.length_3d()
                for point_idx, point in enumerate(segment.points):
                    gpx_data.append([file_idx, os.path.basename(gpx_file), track_idx, track_name,
                                     track_time, track_length, track_duration, track_speed,
                                     seg_idx, segment_length, point.time, point.latitude,
                                     point.longitude, point.elevation, segment.get_speed(point_idx)])
    return gpx_data

# Build a DataFrame
# looped through all of the gpx data and built up a giant two dimensional list of data.
# load that data into a Pandas DataFrame so we can easily sort, filter, group, etc.
gpx_path='/Users/dermotsheridan/Downloads/UCD/Project /garminproject/2021-10-11_garmin_connect_export/'
data = load_gpx_data(gpx_path, filter="")

df = pd.DataFrame(data, columns=['File_Index', 'File_Name', 'Index', 'Name',
                              'Time', 'Length', 'Duration', 'Max_Speed',
                              'Segment_Index', 'Segment_Length', 'Point_Time', 'Point_Latitude',
                              'Point_Longitude', 'Point_Elevation', 'Point_Speed'])

print(df.head())

# detecting the data type of each column automatically.
print(df.dtypes)

# clean up the DataFrame and convert the distances to km
cols = ['File_Index', 'Time', 'Length', 'Duration', 'Max_Speed']
tracks = df[cols].copy()
tracks['Length'] /= 1e3
tracks.drop_duplicates(inplace=True)
print(tracks.head())

tracks['Year'] = tracks['Time'].apply(lambda x: x.year)
tracks['Month'] = tracks['Time'].apply(lambda x: x.month)
tracks_grouped = tracks.groupby(['Year','Month'])
tracks_grouped.describe()

tracks_grouped = tracks.groupby(['Year','Month'])
tracks_grouped['Length'].sum().plot(kind='bar', figsize=(20,15))
plt.xticks(rotation=70)
plt.ylabel('Distance (meters)')
plt.show()