import cPickle as pickle
import sys
import matplotlib.pylab as plt
import numpy as np
import glob
import time
import capo

INTEGRATION_SCALAR = 2**20

def fixpickle(pkl):
    '''Port legacy file format.'''
    data = pkl.pop('data')
    npz = {}
    for k in data[0].keys():
        npz[k] = np.array([di[k] for di in data])
    npz['times'] = pkl['times']
    return npz

data = {}
for file in sys.argv[1:]:
    print 'Reading', file
    #with open(file, 'r') as fh:
        #x = pickle.load(fh)
        #npz = fixpickle(x)
    npz = np.load(file)

    for k in npz.files:
        data[k] = data.get(k,[]) + [npz[k]]

try: freqs = data.pop('freqs')[0]
except(KeyError): freqs = np.arange(0, 250e6, 250e6/512)
times = np.concatenate(data.pop('times'), axis=0)
inttime = data.pop('inttime')
print 'There are %d times in file %s' % (len(times), file)
print 'Start time:'
print time.asctime(time.localtime(times[0]))

f_min = freqs[np.argmin(freqs)]
f_max = freqs[np.argmax(freqs)]
t_min = times[np.argmin(times)]
t_max = times[np.argmax(times)]

for k in data:
    data[k] = np.concatenate(data[k], axis=0).astype(np.complex)

amp_kwargs = {
    'cmap': 'jet',
    #'aspect': 'auto',
    #'interpolation': 'nearest',
    'extent':[f_min,f_max,t_max,t_min]
}

phs_kwargs = {k:val for k,val in amp_kwargs.items()}
phs_kwargs['cmap'] = 'coolwarm'

for cnt,(ant,d) in enumerate(data.items()):
    #if not (ant.endswith('cross') or ant.endswith('auto')): continue
    print ant
    #import IPython; IPython.embed()
    plt.figure(cnt)
    plt.subplot(121)
    capo.plot.waterfall(d/INTEGRATION_SCALAR, mode='log', mx=2, drng=3, **amp_kwargs)
    plt.title('Waterfall Plot -- %s Amplitude' % ant)
    plt.colorbar()
    plt.subplot(122)
    capo.plot.waterfall(d, mode='phs', mx=np.pi, drng=2*np.pi, **phs_kwargs)
    plt.title('Waterfall Plot -- %s Phase' % ant)
    plt.colorbar()

plt.show()

#import IPython; IPython.embed()
