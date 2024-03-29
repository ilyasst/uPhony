from matplotlib.pyplot import *
from scipy import *
from record_to_array import *
from scipy.signal import *
import struct

##get ten seconds of audio data
#data=record_array(10)
#t=linspace(0,10,len(data))

#plot raw data
#figure(1)
#plot(t,data)
#xlabel('Time (s)')
#ylabel('Voltage (V)')
#title('ECG Reading from Heart')

#Adamson's filter
#Define sampling rate and Nyquist frequency
fs=1e4
nyq=fs/2
#Make a copy of the orginal data
original_data=data

#Create a time array
N=len(data)
t=arange(N)*1/fs
#Create a bandpass filter to cut out high and low frequency noise
b,a=butter(2,array([15.,60.])/nyq,'bandpass')
data=filtfilt(b,a,data)
#Create a bandstop filter to remove 60 Hz interference
b,a=butter(1,array([58.,62.])/nyq,'stop')
data=filtfilt(b,a,data)


figure(2)
t=linspace(0,10,N)
clf()
subplot(211)
plot(t,original_data,label="Unfiltered")
legend()
ylabel("Amplitude (V)")

subplot(212)
plot(t,data,label="Filtered")
legend()
xlabel("Time (s)")
ylabel("Amplitude (V)")
show()

#Thresholding
data = data - min(data)
threshold = min(data) + 0.7 * (max(data) - min(data))
print threshold
#if values are below the threshold, eliminate them
for i, vel in enumerate(data):
if vel<threshold:
data[i]=0
#take differential of the slope to find actual maxima
slope = diff(data)
figure(3)
plot(t[:-1],slope)
peak_indices=[]
slope=diff(data)
peak_found=False
for i, vel in enumerate(data):
if vel>0: #If the threshold is exceeded
if peak_found==False: #Only look for peak if not yet found
if ((slope[i]<0 ) and (slope[i-1]>0)): #Look for local maximum
peak_indices.append(i) #Append the peak's index to the list
#print "Found a peak at %fs!" % t[i]
peak_found=True
else:
peak_found=False #Outside the peak so reset the peak_found flag.
#BPM Calculation
print '\n'
time_s_between_beats = [] #create a hold list
for i,val in enumerate(peak_indices):
if i != 0: #to avoid the case when we start iterating and we can't go back one step
time_s_between_beats.append((t[val]-t[peak_indices[i-1]])/60) #add each difference b/t peaks
BPM = 1/mean(time_s_between_beats)
print BPM