import cPickle as pickle
import sys
import matplotlib.pylab as pl
import numpy as np
import glob
import time
import capo

def fixpickle(pkl):
    data = pkl.pop('data')
    npz = {}
    for k in data[0].keys():
        npz[k] = np.array([di[k] for di in data])
    npz['times'] = pkl['times']
    return npz

try:
    fn = sys.argv[1]
    print fn
except IndexError:
    print 'Usage: read_pkl_example.py <filename>'
    exit()

#files = np.sort(glob.glob('/home/kara/documents/hyperion/march_deployment/data/test_correlator_data_03-29-2017_early_am/*.pkl'))
#files = np.sort(glob.glob('/home/kara/documents/hyperion/march_deployment/data/receiver_noise_03-30-2017/*.pkl'))
#files = np.sort(glob.glob('/home/kara/documents/hyperion/march_deployment/data/first_light_03-30-2017_early_morning/*.pkl'))
files = np.sort(glob.glob('/home/kara/src/python/berkeley/Correlator_final/*.pkl'))
print files

for file in files:
    with open(file, 'r') as fh:
        x = pickle.load(fh)
    npz = fixpickle(x)
    #npz = np.load(file)

    times = npz['times']
    frequencies =  (90.0/512) * np.arange(512) + 30
    print frequencies

    print 'There are %d times in file %s' % (len(times), file)

    print 'Start time:'
    print time.asctime(time.localtime(times[0]))

    xx_values = npz['2_auto'].astype(np.float64)
    xy_values = npz['2_11_cross'] 
    yy_values = npz['11_auto'].astype(np.float64)

f_min = frequencies[np.argmin(frequencies)]
f_max = frequencies[np.argmax(frequencies)]
t_min = times[np.argmin(times)]
t_max = times[np.argmax(times)]

pl.figure(0)
pl.subplot(121)
pl.imshow(np.log10(np.abs(xy_values)), aspect='auto', cmap='magma', extent=[f_min,f_max,t_max,t_min])
pl.title('Cross-Correlation Waterfall Plot -- Intensity')
pl.colorbar()
pl.subplot(122)
pl.imshow((np.angle(xy_values)), aspect='auto', cmap='coolwarm', extent=[f_min,f_max,t_max,t_min])
pl.title('Cross-Correlation Waterfall Plot -- Phase')
pl.colorbar()

#pl.figure(1)
#pl.imshow(np.real(xy_values) - np.imag(xy_values), aspect='auto', cmap='magma', extent=[f_min,f_max,t_max,t_min])
#pl.title('Waterfall Plot -- Real Minus Imaginary')

pl.figure(1)
pl.subplot(121)
pl.imshow(np.log10(xx_values/2**20), aspect='auto', cmap='magma', extent=[f_min,f_max,t_max,t_min], interpolation='nearest')
pl.title('Waterfall Plot -- Antenna 6 Auto-Correlation')
pl.colorbar()
pl.subplot(122)
#pl.imshow(np.log10(yy_values), aspect='auto', cmap='magma', extent=[f_min,f_max,t_max,t_min], interpolation='nearest')
capo.plot.waterfall(yy_values/2**20, mode='log', cmap='magma', extent=[f_min,f_max,t_max,t_min])
pl.title('Waterfall Plot -- Antenna 11 Auto-Correlation')
pl.colorbar()
pl.show()

