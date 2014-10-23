import csv
import matplotlib.pyplot as plt
from scipy import *
from scipy.signal import *
import struct
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
from butterworth_recipee import *


def plot_data(name, X, Y):
	plt.plot( X, Y, 'bs' )
	plt.ylabel('Acc')
	plt.xlabel('Time (s)')
	plt.title( name )
	plt.savefig('foo.png')
	plt.show()
	

def design_sleep( time, data_z):

	# Let's start with HBI = 1
	# Paper: Slow-wave sleep estimation on a load-cell-installed bed: a non-constrained method

	# Step 1

	HBI = 1.
	seg_lent = HBI/4.
	seg_lent_list = []
	number_segs = time[ -1] / seg_lent
	print "With HBI = 1, number of segments is:", int( number_segs )

	# Step 2
	maxima = 0
	maximums = []
	
	for i in range( 0, int( number_segs )-1 ):
		max_int = 0
		maximums.append( 0 )
		
		for j in range( 0, len( data_z ) ):
			
			if ( time[j] > number_segs*i) and ( time[j] < number_segs*(i+1) ):
				if ( data_z[j] > max_int ):
					max_int = data_z[j]
				
				if ( j == (len( data_z ) -1) ):
					maximums.append( max_int )
					maxima = maxima+1
				else :
					maximums.append( 0 )
			
			#if ( time[ j ] > number_segs*i) and ( time[ j ] < number_segs*(i+1) ):
				#if ( i == 0 ):
					#maximums.append(i)
				#elif ( data_z[j] > maximums[i] ):
					#maximums[i ] = data_z[j]
				#else:
					#pass

				
			#print "The maximum for [", number_segs*i, ";", number_segs*(i+1), "] is:", maximums[i]


	# Step 3

	X = []
	print "Len(maximums) and Len(number_segs) should be the same, check it here"
	print len(maximums), len(seg_lent_list)

	for i in range( 0, len( maximums )-1 ):
		if ( maximums[i] != 0 ):
			
			if ( i == 0 ):
				if (maximums[0] > maximums[1]):	
					X.append( maximums[i] )
				else:
					X.append( 0 )
			elif ( i == len( maximums ) ):
				if (maximums[-1] > maximums[-2]):
					X.append( maximums[-1] )
				else:
					X.append( 0 )
			else:
				if ( maximums[ i ] > maximums[ i - 1 ]) and ( maximums[ i ] > maximums[ i + 1 ]):
					X.append( maximums[i] )
					print "X[", i, "] seems to be a local maximum =", maximums[i]
				else:
					X.append( 0 )	
		else:
			X.append( 0 )


	# Step 4
	Y = []
	
	for i in range( 0, len( X )-1 ):
		if X[i] != 0:
			Y.append( seg_lent*i )
	
	k = 0
	for j in range( 0, len(Y)-2 ):
		if ( Y[j+1] - Y[j] < (HBI/2.) ) or ( Y[j+2] - Y[j+1] < (HBI/2.) ):
			print "NOT POSSIBLE HB"
			k = k + 1 
			
			#e = min( Y[i], Y[i+1], Y[i+2] )
			
			#if ( e == Y[i]):
				#Y[i] = 0
			#elif (e == Y[i+1]):
				#Y[i+1] = 0
			#elif ( e == Y[i+1]):
				#Y[i+2] = 0

	print "Number of peaks = ", k
	pulse = (float(k) / float(time[-1]) )*60
	print "Pulse should be:", pulse
	print "step1" , maxima
	return pulse

data_x = []
data_y = []
data_z = []
time = []
angle_list = []
i = 0

import math

#for angle in xrange( 0, 3600, 5):
	#y = math.sin(math.radians(angle))
	#data_z.append( y )
	#angle_list.append( angle )
			
#plot_data( "sine test", angle_list , data_z)

with open('chestband_calm.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		if (row[0] == "#"):
			pass
		else:
			data_x.append( float(row[0]) )
			data_y.append( float(row[1]) )
			data_z.append( float(row[2]) )
			time.append( float(row[3])*float(i)*0.001 )

			i = i + 1
			
			
filtered_data_z = butter_bandpass_filter(data_z, 0.5, 2., 200., order=2)

data_z_filtfilt = filtered_data_z 

#d, c = butter(2, array([.8,1.2])/(200*0.5) ,'stop')
#data_z_bandstopped = filtfilt(d, c, filtered_data_z )

plot_data( "Original Data", time , data_z)
plot_data( "Recipee", time , filtered_data_z)
#plot_data( "Bandstopeed and passband", time , data_z_bandstopped)


	#Thresholding
#data_z_filtfilt = data_z_filtfilt - min(data_z_filtfilt)
#threshold = min(data_z_filtfilt) + 0.4* ( max(data_z_filtfilt) - min(data_z_filtfilt) )
#print i, "Thresholding=", threshold 
#plot_data( "Threshold", time , filtered_data_z)

	##if values are below the threshold, eliminate them
#for j, vel in enumerate(data_z_filtfilt):
		#if vel < threshold:
			#data_z_filtfilt[j]=0
			
##take differential of the slope to find actual maxima
#peak_indices = []
#slope = diff(data_z_filtfilt)
#peak_found = False
#print "Slope length", len(slope)

#for k, vel in enumerate(data_z):
		#if vel > 0: #If the threshold is exceeded
			#if peak_found==False: #Only look for peak if not yet found
				#if k == len(slope):
					#peak_found = False
				#elif ((slope[k]<0 ) and (slope[k-1]>0)): #Look for local maximum
					#peak_indices.append(k) #Append the peak's index to the list
					#print "Found a peak at %fs!" % time[k]
					#peak_found=True
		#else:
			#peak_found = False #Outside the peak so reset the peak_found flag.

	##BPM Calculation
#print '\n'
		
#time_s_between_beats = [] #create a hold list

#for l,val in enumerate(peak_indices):
		#if l != 0: #to avoid the case when we start iterating and we can't go back one step
			#time_s_between_beats.append((time[val]-time[peak_indices[l-1]])/60) #add each difference b/t peaks
			
#BPM = 1./mean(time_s_between_beats)
#print i, "BPMs = ", BPM

design_sleep( time, data_z)


			
