import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.optimize import curve_fit
from scipy.optimize import leastsq
import glob
import argparse 
import threading

files = glob.glob("crab(htoh)/crabspecs*")
files = sorted(files)

specs = {f[:-4]: np.load(f, allow_pickle=True)["corr01"] for f in files}
acc_cnt = {f[:-4]: np.load(f, allow_pickle=True)["acc_cnt"] for f in files}
times = {f[:-4]: np.load(f, allow_pickle=True)["time"] for f in files}

data = []
for keys in specs.keys():
    data.append(specs[keys])

#print(data)
timings = []
for k in times.keys():
    timings.append(times[k])

#fdata = data[...,0]+1j*data[...,1]
#print(fdata)

real = []
imagin = []
for i in np.arange(len(data)):
    real.append(data[i].real)
    imagin.append(data[i].imag)

data = np.array(data)
print(len(data))
print(len(real))
print(len(imaging))


plt.figure(figsize = (12,6))

plt.plot(real[50])
plt.plot(imagin[50])
#plt.ylim(0,50)
plt.xlabel("Frequency")
plt.ylabel("Power")
plt.show()

plt.figure(figsize = (12,6))
plt.imshow(np.abs(data), cmap='magma', vmin=0, vmax = 3)
plt.colorbar()

plt.figure(figsize = (12,6))
plt.imshow(np.angle(data), cmap='magma', vmin=0, vmax = 3)
plt.colorbar()

