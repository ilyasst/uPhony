from scipy import signal
from scipy.signal import *
import matplotlib.pyplot as plt

def plot_data(name, X, Y):
	plt.plot( X, Y, 'r--' )
	plt.ylabel('Acc')
	plt.xlabel('Time (s)')
	plt.title( name )
	plt.savefig('foo.png')
	plt.show()

t = np.linspace(0, 1., 10001)
xlow = np.sin(2 * np.pi * 5 * t) 
xhigh = np.sin(2 * np.pi * 250 * t)
x = xlow + xhigh

plot_data("Whatever", t, x )

b, a = signal.butter(8, 0.125)
y = signal.filtfilt(b, a, x, padlen=150)
print np.abs(y - xlow).max()

plot_data("Whatever", x, y)