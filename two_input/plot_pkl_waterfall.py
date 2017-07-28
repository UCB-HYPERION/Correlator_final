import cPickle as pickle
import sys
import matplotlib.pylab as pl
import numpy as np
import glob
import time

xx_values = []
xy_values = []
yy_values = []

for file in sys.argv[1:]:
    with open(file, 'r') as fh:
        x = pickle.load(fh)

    times = x['times']
    data  = x['data']
    frequencies = np.linspace(0,125,512) 

    print 'There are %d times in file %s' % (len(times), file)

    print 'Start time:'
    print time.asctime(time.localtime(times[0]))

    print 'Data dictionary has keys:'
    print data[0].keys()

    for i in np.arange(len(times)):
        xx_values.append(data[i]['xx'])
        xy_values.append(data[i]['xy'])
        yy_values.append(data[i]['yy'])

f_min = frequencies[np.argmin(frequencies)]
f_max = frequencies[np.argmax(frequencies)]
t_min = times[np.argmin(times)]
t_max = times[np.argmax(times)]

mean = np.mean(xy_values, axis=1)
pl.figure(0)
pl.subplot(121)
#pl.imshow(np.log10(np.abs(xy_values)), aspect='auto', extent=[f_min,f_max,t_max,t_min])
#pl.imshow(np.log10(np.abs(xx_values)), aspect='auto', cmap='magma', extent=[f_min,f_max,t_max,t_min], interpolation='nearest')
pl.plot(np.log10(np.abs((xx_values[10]))))
#pl.plot(np.log10(np.abs((mean))))
pl.title('Waterfall Plot -- Intensity')
#pl.colorbar()
pl.subplot(122)
#pl.imshow((np.angle(xy_values)), aspect='auto', extent=[f_min,f_max,t_max,t_min])
pl.imshow((np.angle(xy_values)), aspect='auto', cmap='coolwarm', extent=[f_min,f_max,t_max,t_min], interpolation='nearest')
pl.title('Waterfall Plot -- Phase')
pl.colorbar()

pl.show()

