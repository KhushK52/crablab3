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
parser = argparse.ArgumentParser()
parser.add_argument('--filename', '-n', help='name to give file')


#parser to name files more conviniently
args = parser.parse_args()
file = args.filename


#start dictionary of dates
julians = {}

#start keeping track of keys for julians dictionary
num = 0

#connect to those girls (the girls being the dishes)
ifm = ugradio.interf.Interferometer()


#now we want to track the Sun

try:
    while True:
            num += 1 
            jd = ugradio.timing.julian_date()   #get the new Julian date after pointing at the sun initially
            julians.update({num:jd})
            #first we want to find the Sun
            #get the altitude and azimuth of the sun at the given jd. Got precessed to correct for precession of equinox 
            ra, dec = ugradio.coord.sunpos(jd = jd)
            pra, pdec = ugradio.coord.precess(ra = ra, dec = dec, jd=jd)
            alt, az = ugradio.coord.get_altaz(ra = pra, dec = pdec, jd=jd)   #ugradio.coord.get_altaz(pra, pdec, jd, lat, lon, alt) default for lat,lon,alt is nch
        
            #point the big bois
            if az <= 90:
                ifm.point(az=az+180, alt=alt+90)
            if az >= 300:
                ifm.point(az=az-180, alt=alt+90)
            else: 
                ifm.point(alt, az)

            print("I do be pointing")
            time.sleep(30)   #gives a delay of 30s before it starts running the code again
except KeyboardInterrupt:
    print("That's enough! You stopped pointing")
    np.savez(f'{file}.npz', dates=julians)
   
    # stops running the script when u press Ctrl C



