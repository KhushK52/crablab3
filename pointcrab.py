import ugradio
import snap_spec
import numpy as np
import matplotlib.pyplot as plt
import astropy
import time
from scipy.optimize import curve_fit
from scipy.optimize import leastsq
import glob
import argparse 
import threading
parser = argparse.ArgumentParser()
parser.add_argument('--filename', '-n', help='name to give file')
parser.add_argument('--record_time', '-t', type = int, help='length of time to take data for')

#parser to name files more conviniently
args = parser.parse_args()
file = args.filename
record_time = args.record_time

ifm = ugradio.interf.Interferometer()

spec = snap_spec.snap.UGRadioSnap()
spec.initialize(mode='corr') 

running = True 

def crab_pointing(): 
    global running 
    #start dictionary of dates
    julians = {}
    #start keeping track of keys for julians dictionary
    num = 0
    #now we want to track the crab
    while running:
            num += 1 
            jd = ugradio.timing.julian_date()   #get the new Julian date after pointing at crab initially
            julians.update({num:jd})
            #first we want to find Crab
            #get the altitude and azimuth of crab at the given jd. Got precessed to correct for precession of equinox 
            ra, dec = 83.633125, 22.01447222 
            pra, pdec = ugradio.coord.precess(ra = ra, dec = dec, jd=jd)
            alt, az = ugradio.coord.get_altaz(ra = pra, dec = pdec, jd=jd)   #ugradio.coord.get_altaz(pra, pdec, jd, lat, lon, alt) default for lat,lon,alt is nch

            #point the big bois
            if az <= 90:
                ifm.point(az=az+180, alt=(180-2*alt)+alt)
            if az >= 300:
                ifm.point(az=az-180, alt=(180-2*alt)+alt)
            else: 
                ifm.point(alt, az)

            print("I do be pointing")
            time.sleep(30)   #gives a delay of 30s before it starts running the code again
    print("That's enough! You stopped pointing")
    np.savez(f'{file}dates.npz', dates=julians)
        # stops running the script when u press Ctrl C


def read():
    global running
    count = None 
    while running:
        try: 
            data=spec.read_data(prev_cnt=count)
            np.savez(f'{file}specs{count}', **data)
            count = data['acc_cnt']
        except(AssertionError):
            count = None


def duration(mins):
    global running
    time.sleep(mins * 60)
    running = False


#first pointing at Crab 
jd = ugradio.timing.julian_date()   
ra, dec = 83.633125, 22.01447222 
pra, pdec = ugradio.coord.precess(ra = ra, dec = dec, jd=jd)
alt, az = ugradio.coord.get_altaz(ra = pra, dec = pdec, jd=jd)
if az <= 90:
    ifm.point(az=az+180, alt=(180-2*alt)+alt)
if az >= 300:
    ifm.point(az=az-180, alt=(180-2*alt)+alt)
else: 
    ifm.point(alt, az)

thread = threading.Thread(target=read, daemon = True)
time_thread = threading.Thread(target=duration, args = (record_time,), daemon = True)

thread.start()
time_thread.start()

crab_pointing()

"""
converting the given crab coordinates to degrees so itll work with the rest of ugradio.coord code 

given 
ra = {h = 5 , m = 34, s = 31.95}
dec = {def = 22, o = 0 , n = 52.1}

JK JK I FIGURED IT OUT!!!

from online source:
ra , dec = 	184.5551 , -05.7877   but is this right?? --> i dont think this is right lmao 

SkyCoord('05h34m31.95s +22d00m52.1s') --> for crab 
<SkyCoord (ICRS): (ra, dec) in deg
    (83.633125, 22.01447222)

therefore for crab:
ra = 83.633125
dec = 22.01447222 

jd = ugradio.timing.julian_date()   
ra, dec = 83.633125, 22.01447222 
pra, pdec = ugradio.coord.precess(ra = ra, dec = dec, jd=jd)
alt, az = ugradio.coord.get_altaz(ra = pra, dec = pdec, jd=jd)

and then just use all the other code!! if it works ... 
i really really hope it works! 
"""