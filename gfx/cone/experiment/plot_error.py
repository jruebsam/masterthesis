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

def main():
    dpath = '/home/upgp/jruebsam/simulations/mai16/week2/cone_wall/data/omg_1.00/gfx'

    f, ax = style.newfig(0.6, 1.)

    with tb.open_file(os.path.join(dpath, "00001000.h5"))as d:
        vz = d.root.xz.vz[64]
        vz2 = d.root.xy.vz[64]

    x = np.linspace(0, 1, len(vz))
    plt.plot(x, vz, lw =0.5, label='$x,z=0.5$')
    x = np.linspace(0, 1, len(vz2))
    plt.plot(x, vz2, lw =0.5, label='$x,y=0.5$')

    #ax.set_ylim(0., 0.04)
    #ax.set_xlim(0.15, 2.05)
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-3,-2))
    ax.yaxis.set_major_formatter(formatter)

    ax.set_xlabel(r'Position', labelpad=0)
    ax.set_ylabel(r'$v_z$', labelpad=0)

    plt.legend(ncol = 2, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.3),
           fancybox=True, shadow=True)

    plt.subplots_adjust(top=0.8, bottom =0.15)

    plt.savefig('error.pdf')

if __name__=='__main__':
    main()
