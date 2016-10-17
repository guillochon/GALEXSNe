import csv
import json

import gPhoton.gAperture
import numpy as np
from astropy import units as un
from astropy.coordinates import SkyCoord as coord
from astropy.time import Time as astrotime

with open('ess-sne.csv', 'r') as f:
    rows = list(csv.reader(f, delimiter=',', quotechar='"'))
datas = []
for ri, row in enumerate(rows[1:]):
    if ri >= 10:
        break
    ddate = row[1].split(',')[0]
    ra = row[2].split(',')[0]
    dec = row[3].split(',')[0]
    if not ddate or not ra or not dec:
        continue
    coo = coord(ra=ra, dec=dec, unit=(un.hourangle, un.deg))
    dra, ddec = coo.ra.deg, coo.dec.deg
    gtime = astrotime(ddate.replace('/', '-')).unix - 315964800.
    tmin = gtime - 86400. * 365.0
    tmax = gtime + 2.0 * 86400. * 365.0
    try:
        data = gPhoton.gAperture(
            band='NUV',
            skypos=[dra, ddec],
            radius=0.03,
            annulus=[0.03, 0.04],
            trange=[tmin, tmax],
            stepsz=600.)
    except:
        data = None
    if data is not None:
        for key in data:
            if isinstance(data[key], np.ndarray):
                data[key] = data[key].tolist()
        del data['photons']
        data['name'] = row[0]
        datas.append(data)
        print('Found data for {}!'.format(row[0]))
    else:
        print('{} has no data, skipping.'.format(row[0]))
with open('gdict.json', 'w') as f:
    f.write(json.dumps(datas))
