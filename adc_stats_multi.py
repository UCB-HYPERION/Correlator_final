#	Eddie Toral
#	CAMPARE Summer 2016 Research Undergrad
#	August 16th, 2016
#	
#	Simple model used to obtain data to determine analog input level to digital output level relationship.
#	75.0 MHz single tone from input levels +12dBm to -36.0 dBm.
#	Direct connection to input of SNAP Board, no attenuators or filters used during testing.
#	Only 1 antenna at a time, selectable by [option] -a to be selected when running script
#	adc_stats_2016-8-16_1606.bof

#from argparse import ArgumentParser
#p = ArgumentParser(description = 'python adc_stats.py [options] ')
#p.add_argument('host', type = str, default = '10.0.1.217', help = 'Specify the host name')
#p.add_argument('-a', '--antenna', dest = 'antenna', type = int, default = 0, help = 'antenna selection')

#args = p.parse_args()
#host = args.host
#antenna = args.antenna

host = 'rpi2-3'
antenna = 2
scale = 4096

import corr, struct, numpy as np, matplotlib.pyplot as plt, time
s = corr.katcp_wrapper.FpgaClient(host,7147,timeout = 10)
time.sleep(1)
scale_ant = 'scale{x}'.format(x=antenna)
s.write_int(scale_ant, scale)
s.write_int('prequant_select', antenna)
s.write_int('postquant_select', antenna)
s.write_int('prequant_ctrl', 1)
s.write_int('postquant_ctrl', 1)
s.write_int('prequant_ctrl', 0)
s.write_int('postquant_ctrl', 0)

# NOTE: maybe add actual adc snapshot block to look at the incoming rms, sanity 
# check?

prequant_data = s.snapshot_get('postquant',man_trig=True,man_valid=True)
preq = struct.unpack('>2048d',prequant_data['data'])
preq = np.asarray(preq)
postquant_data = s.snapshot_get('postquant',man_trig=True,man_valid=True)
postq = struct.unpack('>2048b',postquant_data['data'])
postq = np.asarray(postq)

preq_sigma = np.sqrt(np.var(preq))
print "Hey this one is the preequalization sigma"
print preq_sigma

preq_rms = np.sqrt(np.mean(np.square(preq)))
print "Hey this one is the preequalization rms"
print preq_rms

postq_sigma = np.sqrt(np.var(postq))
print "Hey this one is the postequalization sigma"
print postq_sigma

postq_rms = np.sqrt(np.mean(np.square(postq)))
print "Hey this one is the postequalization rms"
print postq_rms

#plt.figure(1)
#plt.title('Adc Data: Antenna 0')
#plt.plot(ad,'k')
#plt.axis([0,65535,-136,135])
#plt.grid(True)

#plt.figure(2)
#plt.hist(ad, bins=256) 
#plt.title("Histogram with 256 bins")
#plt.show()