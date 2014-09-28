
def design_sleep( time, data_z):

# Let's start with HBI = 1
# Paper: Slow-wave sleep estimation on a load-cell-installed bed: a non-constrained method

# Step 1

HBI = 1.
seg_lent = HBI/4.
seg_lent_list = []
number_segs = time[ -1] / seg_lent
print "With HBI = 1, number of segments is:", seg_lent

# Step 2

maximums = []
for i in range( 0, number_segs ):
	 for j in range( 0, len( data_z) ):
		if ( time[j] > number_segs[i]) and ( time[j] < number_segs[i+1] ):
			if maximums[i] = 0:
				maximums[i ] = data_z[j]
			elif ( data_z[j] > maximums[i] ):
				maximums[i ] = data_z[j]
			else:
				pass
	print "The maximum for [", i, ";", i+1, "] is:", maximums[i]


# Step 3

X = []
Y = [] 
print "Len(maximums) and Len(number_segs) should be the same, check it here"
print len(maximums), len(number_segs)

for i in range( 0, len( maximums ) ):
	if ( i = 0 ):
		X[0] = maximums[i]
		Y[0] = X[0]
	elif ( i = len( maximums ) ):
		X[len(maximums)] = maximums[ -1 ]
		Y[len(maximums)] = maximums[ -1 ]
	else:
		if ( maximums[ i ] > maximums[ i - 1 ]) and ( maximums[ i ] > maximums[ i + 1 ]):
			X[ i ] = maximums[i]
			Y[ i ] = maximums[i]
 			print "X[", i, "] seems to be a local maximum =", maximums[i]
		else:
			X[ i ] = 0
			Y[i ] = 0

# Step 4

print "Len(maximums) and Len(X) should be the same, check it here"
print len(maximums), len(X)

for i in range( 0, len( X ) ):
	if ( Y[i+1] - Y[i] < (HBI/2.) ) or ( Y[i+2] - Y[i+1] < (HBI/2.) ):
		e = min( Y[i], Y[i+1], Y[i+2] )
		if e = Y[i]):
			Y[i] = 0
		elif (e = Y[i+1]):
			Y[i+1] = 0
		elif ( e = Y[i+1]):
			Y[i+2] = 0

print "Number of peaks = ", len(Y)
print "Pulse should be:", float(len(Y))/time[-1]


 