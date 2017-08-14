#import corr, struct, numpy as np, matplotlib.pyplot as plt, time
import casperfpga, struct, numpy as np, matplotlib.pyplot as plt, time

host = '10.10.10.101'
antenna = 4
scale = 4
#scale = 4096

def reinterpret(v):
    return struct.unpack('b',struct.pack('B',v))[0]

#s = corr.katcp_wrapper.FpgaClient(host,7147,timeout = 10)
s = casperfpga.CasperFpga(host,7147,timeout = 10)
time.sleep(1)
s.write_int('antenna', antenna)
scale_ant = 'scale{x}'.format(x=antenna)
s.write_int(scale_ant, scale)
s.write_int('prequant_select', antenna)
s.write_int('postquant_select', antenna)
s.write_int('prequant_ctrl', 1)
s.write_int('postquant_ctrl', 1)
s.write_int('prequant_ctrl', 0)
s.write_int('postquant_ctrl', 0)
s.write_int('adc_stats_ctrl', 1)
s.write_int('adc_stats_ctrl', 0)

# NEED TO MODIFY SNAPSHOTS TO FIT CASPERFPGA
adc_stats = s.snapshot_get('adc_stats',man_trig=True,man_valid=True)
stats = struct.unpack('>256b',adc_stats['data'])
stats = np.asarray(stats)
prequant_data = s.snapshot_get('prequant',man_trig=True,man_valid=True)
preq = struct.unpack('>512q',prequant_data['data'])
postquant_data = s.snapshot_get('postquant',man_trig=True,man_valid=True)
postq = struct.unpack('>512B',postquant_data['data'])

# move bits around to make numbers readable in python
tpreq = []
bpreq = []
preq_rms = 0
for each in preq:
    top = (each >> 18) & 0x3FFFF
    if top > 2**35-1:
        top = -(2**36-top)
    tpreq.append(top)
    bot = each & 0x3FFFF
    if bot > 2**35-1:
        bot = -(2**36-bot)
    bpreq.append(bot)
    preq_rms += top**2 + bot**2
preq_real = np.asarray(tpreq)
preq_imag = np.asarray(bpreq)
tpostq = []
bpostq = []
postq_rms = 0
for each in postq:
    top = reinterpret(each & 0xF0) >> 4
    tpostq.append(top)
    bot = reinterpret((each & 0x0F) << 4) >> 4
    bpostq.append(bot)
    #top = (each >> 4) & 0x0F
    #if top > 2**3-1:
    #    top = -(2**4-top) + 1
    #    print top
    #tpostq.append(top)
    #bot = each & 0x0F
    #if bot > 2**3-1:
    #    bot = -(2**4-bot) + 1
    #bpostq.append(bot)
    postq_rms += top**2 + bot**2
postq_real = np.asarray(tpostq)
postq_imag = np.asarray(bpostq)

rms = np.sqrt(np.mean(np.square(stats)))
print "Hey this one is the ADC rms"
print rms

preq_rms = np.sqrt(1.0*preq_rms/len(preq_real))
print "Hey this one is the prequantization rms"
print preq_rms

postq_rms = np.sqrt(1.0*postq_rms/len(postq_real))
print "Hey this one is the postquantization rms"
print postq_rms

plt.figure(1)
title = 'ADC Data: Antenna {i}'.format(i=antenna)
plt.title(title)
plt.plot(stats,'k')
plt.axis([0,256,-136,135])
plt.grid(True)

plt.figure(2)
plt.hist(stats, bins=256) 
plt.title("Histogram with 256 bins")

plt.figure(3)
title = 'Pre-Quantization Data: Antenna {i}'.format(i=antenna)
plt.title(title)
plt.plot(preq_real,'r', label='real')
plt.plot(preq_imag,'b', label='imag')
#plt.axis([0,256,-68719476736,68719476735])
plt.grid(True)

plt.figure(4)
plt.hist(preq, bins=256) 
plt.title("Histogram with 256 bins")

plt.figure(5)
title = 'Post-Quantization Data: Antenna {i}'.format(i=antenna)
plt.title(title)
plt.plot(postq_real,'r', label='real')
plt.plot(postq_imag,'b', label='imag')
plt.legend()
#plt.axis([0,256,-136,135])
plt.grid(True)

plt.figure(6)
plt.hist(postq, bins=256) 
plt.title("Histogram with 256 bins")
plt.show()
