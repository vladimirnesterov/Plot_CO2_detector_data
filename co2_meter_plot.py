# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 22:16:52 2021
@author: vladimirnesterov

This script's purpose is to parse and plot data of a 
"Carbon dioxide detector" from Aliexpress. From the one that can export
recorded data into pdf files.
 
The script takes all pdf files that were exported from CO2 meter 
and located in the same directory with this script. 
For correct plotting setup the parameters of date and time 
into the beginning of the script.

*The CO2 meters may record data with not existed dates as it seems has 
always 31 day in every month. This script doesn't handle this situation
and will just through away that day.

"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import scipy.signal as signal
import datetime
import os

#################### setup ########################
# Date and time to start and finish plotting
# in dormat (year, month, day, hour, minute, second)
min_date = datetime.datetime(2021, 6, 21, 10, 0, 0)
max_date = datetime.datetime(2021, 6, 25, 19, 0, 0) 

###################################################

# variables
record_number       = []
co2_data            = []
temperature_data    = []
humidity_data       = []
time_data           = []
file_names          = []
previous_date = min_date

# get all files
my_dir = os.path.dirname(__file__)
all_files = [f for f in os.listdir(my_dir) if os.path.isfile(os.path.join(my_dir, f))]
for file in all_files:
    if (file[-4:] == ".pdf"):
        file_names.append(file)       

# Parse pdf files one by one
for record_file in file_names:
   
    F = open(record_file,'r') 
    for line in F.readlines():     
        try:
            A = list(map(str, line.split()))
            if (len(line) > 60):
                if (len(A) == 7):
                    record_number.append(int(A[0][1:]))
                    
                    date = A[1].split('/')
                    time = A[2].split(":")
                    current_record_time = datetime.datetime((int(date[0])), int(date[1]), int(date[2])+1, int(time[0]), int(time[1]), int(time[2]))
                    if (current_record_time > min_date and current_record_time < max_date and current_record_time > previous_date):
                        time_data.append(current_record_time)
                        co2_data.append(int(A[3]))
                        temperature_data.append(float(A[4]))
                        humidity_data.append(float(A[5][:-1]))
                        previous_date = current_record_time
        except: 
            print(A)
            print("oops")
    
    F.close()
   
# filter data 
b, a = signal.butter(3, 0.2, 'low')
co2_data = signal.filtfilt(b, a, co2_data)

# plot data
fig_co2 = plt.figure()
ax_co2 = fig_co2.add_subplot(111)
ax_co2.plot_date(time_data, co2_data, linewidth=3.5, linestyle='solid', marker='None')

# Beautify the plot 
fig_co2.suptitle("CO2 recordings in the office", fontsize=18)
ax_co2.set_xlabel('Date-time [month-day hour]', fontsize=18)
ax_co2.set_ylabel('CO2 level', fontsize=18)
ax_co2.axhspan(300, 400,  facecolor='lime',         alpha=0.8)
ax_co2.axhspan(400, 600,  facecolor='greenyellow',  alpha=0.8)
ax_co2.axhspan(600, 800,  facecolor='orange',       alpha=0.7)
ax_co2.axhspan(800, 1000, facecolor='red',          alpha=0.6)
outdoor_zone   = mpatches.Patch(color='lime',        label='Normal outdoor level')
okindoor_zone  = mpatches.Patch(color='greenyellow', label='Acceptable indoor level')
notokdoor_zone = mpatches.Patch(color='orange',      label='May feel stuffiness and odors')
badindoor_zone = mpatches.Patch(color='red',   label='May feel sleepy and headache')
ax_co2.legend(handles=[badindoor_zone,notokdoor_zone,okindoor_zone,outdoor_zone], loc='upper left')

plt.show()
