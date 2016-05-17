import style
style.setup()
import matplotlib
matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
from matplotlib.patches import Polygon
from matplotlib import ticker

import numpy as np
import matplotlib.pyplot as plt
import os, sys
from glob import glob
import tables as tb
import pycurb.analysis as pa
from scipy import stats
import itertools as it
import itertools
from scipy import optimize
from scipy.ndimage import gaussian_filter as gf


cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']
markers = itertools.cycle('o^*')

from cycler import cycler

cc = itertools.cycle(plt.cm.spectral(np.linspace(0,1,10)))
#plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def get_amp(series):
    n = len(series)/4
    data = series[3*n:]
    A = 0.5*(np.max(data)-np.min(data))
    return A

def main():
    dpath = '/home/upgp/jruebsam/simulations/mai16/week2/cone_wall/data/omg_1.00/gfx'

    f, ax = style.newfig(0.6, 1.)

    with tb.open_file(os.path.join(dpath, "00001000.h5"))as d:
        vz = d.root.xz.vz[:]

    filtered = gf(vz, sigma=1.3)
    #cs = ax.contourf(filtered.T, 50, origin='lower',extent=[0, 1, 0,1 ] )
    im =  ax.imshow(filtered.T, origin='lower',extent=[0, 1, 0.25, 1 ] )
    ax.contour(filtered.T, 20, origin='lower',extent=[0, 1, 0.25,1 ],\
                        colors='k', linewidths=(0.5,))

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3,-2))

    cb = plt.colorbar(im,  pad=0., format=formatter)
    cb.set_label(r'$v_z$')

    x = [0, 0.5, 1]
    y = [1, 0.25, 1]
    plt.plot(x,y, 'r')

    hc = 0.5*np.tan(np.pi/3.) -0.25
    r = 0.25*np.tan(np.pi/6.)

    p = Polygon([[0, 0.25],[0.5 - r, 0.25],[0, hc + 0.25]], color='w', hatch='//', zorder=4)
    ax.add_artist(p)
    p = Polygon([[1., 0.25],[0.5 + r, 0.25],[1, hc + 0.25]], color='w', hatch='//', zorder=4)
    ax.add_artist(p)

    #ax.set_ylim(0., 0.04)
    #ax.set_xlim(0.15, 2.05)
    ax.set_xlabel(r'$x$', labelpad=-5)
    ax.set_ylabel(r'$z$', labelpad=-5)
    ax.set_xticks([0,  1])
    ax.set_yticks([0.25, 0.5, 0.75, 1])

    #plt.subplots_adjust(bottom =0.2)
    plt.tight_layout()
    plt.savefig('contour.pdf')

if __name__=='__main__':
    main()
