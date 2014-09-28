import csv
import matplotlib.pyplot as plt
from scipy import *
from scipy.signal import *
import struct

def plot_data(name, X, Y):
	plt.plot( X, Y, 'bs' )
	plt.ylabel('Acc')
	plt.xlabel('Time (s)')
	plt.title( name )
	plt.savefig('foo.png')
	plt.show()


print "==============================="
print "I love UPhony"
print "==============================="

data_x = []
data_y = []
data_z = []
time = []
i = 0

with open('Irenee-chest-test.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	print row[0]
	for row in spamreader:
		if (row[0] == "#"):
			pass
		else:
			data_x.append( float(row[0]) )
			data_y.append( float(row[1]) )
			data_z.append( float(row[2]) )
			time.append( float(row[3])*float(i)*0.001 )

			i = i + 1
	

	frequency = 1. / ( time[1] )
	
	#plot_data( "pulse-ilyass-armband_X" ,time, data_x )
	#plot_data( "pulse-ilyass-armband_Y" ,time, data_y )
	#plot_data( "pulse-ilyass-armband_Z" ,time, data_z )

	
N=len(data_z)
print "Length Z=", N

#time= 0 to N*5us
Ny_freq = frequency / 2.
print "Nyquist =", Ny_freq
print "Frequency=", frequency

# for i in range(10, int(Ny_freq), 5):
#	print "COUNT =", i
#	i_float = float(i)
#	print i_float/Ny_freq
#b, a = butter(5,array([0.4,0.8])/Ny_freq,'lowpass')
b, a = butter(5,.008,'lowpass')
	#print "B =", b
	#print "A =", a
	#print "Type z=", type( data_z)
	#print "Type b=", type( b)
	#print "Type a=", type( a)
	#print "Type z[0]=", type( data_z[0])


data_z_filtfilt = filtfilt( b, a, data_z )
	
#b, a = butter(1, i_float/Ny_freq, 'highpass')
	
#	data_z_filtfilt = filtfilt( b, a, data_z_filtfilt )

	#plot_data( "pulse-ilyass-armband_Z", time, data_z )
plot_data( "pulse-ilyass-armband_Z_filtered" ,time, data_z_filtfilt )

	#Create a bandstop filter to remove 60 Hz interference
b, a = butter(2, array([58.,62.])/Ny_freq ,'stop')
data_z_filtfilt = filtfilt(b, a, data_z_filtfilt )
plot_data( "pulse-ilyass-armband_Z_filtered_2" ,time, data_z_filtfilt )
#has band stop



	#Thresholding
data_z_filtfilt = data_z_filtfilt - min(data_z_filtfilt)
threshold = min(data_z_filtfilt) + 0.4* ( max(data_z_filtfilt) - min(data_z_filtfilt) )
print i, "Thresholding=", threshold 

	#if values are below the threshold, eliminate them
for j, vel in enumerate(data_z_filtfilt):
		if vel<threshold:
			data_z_filtfilt[j]=0
			
	#take differential of the slope to find actual maxima
slope = diff(data_z_filtfilt)
plot_data( "Slope", time[:-1],slope )
peak_indices = []
slope = diff(data_z_filtfilt)
peak_found = False

for k, vel in enumerate(data_z):
		if vel>0: #If the threshold is exceeded
			if peak_found==False: #Only look for peak if not yet found
				if ((slope[k]<0 ) and (slope[k-1]>0)): #Look for local maximum
					peak_indices.append(k) #Append the peak's index to the list
					#print "Found a peak at %fs!" % time[i]
					peak_found=True
		else:
			peak_found=False #Outside the peak so reset the peak_found flag.

	#BPM Calculation
print '\n'
		
time_s_between_beats = [] #create a hold list

for l,val in enumerate(peak_indices):
		if l != 0: #to avoid the case when we start iterating and we can't go back one step
			time_s_between_beats.append((time[val]-time[peak_indices[l-1]])/60) #add each difference b/t peaks
			
BPM = 1/mean(time_s_between_beats)
print i, "BPMs = ", BPM




	
			
