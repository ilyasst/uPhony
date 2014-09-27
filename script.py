import csv

print "==============================="
print "I love UPhony"
print "==============================="

data_x = []
data_y = []
data_z = []
time = []
i = 0

with open('Pulse-ilyass-armband-fastest-220fps.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		if (row[0] == "#"):
			pass
		else:
			data_x.append( row[0] )
			data_y.append( row[1] )
			data_z.append( row[2] )
			time.append( float(row[3]) )
			
			with open('Pulse-ilyass-armband-fastest-220fps_clean.csv', 'wb') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
				spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])

			
			i = i + 1

		
		#print ', '.join(row)

