import style as style
style.setup()

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

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

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
    dpath = '/home/upgp/jruebsam/simulations/april16/week2/cylinder_series/data/df/o2'
    f, ax = style.newfig(1., 0.6)
    modes = list(it.product(['df', 'vp', 'dffrac', 'vpfrac'], [1, 0]))

    omgs = [1.2, 0.5]
    for omg in omgs:
        dp = os.path.join(dpath, 'omg_%.1f' % omg, 'omg_%.1f.ekin' % omg)


        data = np.genfromtxt(dp)
        time = data[:, 0]
        vz = data[:, -3]

        ax.plot(time, vz, lw=0.8, label = r'$\omega=%.1f$' % omg)

    ax.set_ylim(0., 2.8*1e-3)
    ax.set_xlabel(r'time')
    ax.set_ylabel(r'$\left<v_z^2\right>$')
    plt.legend(ncol = 2, fontsize=8, loc='upper left',
           fancybox=True, shadow=True)

    plt.subplots_adjust(bottom =0.15)
    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2,-3))
    ax.yaxis.set_major_formatter(formatter)

    ax.grid(True)
    plt.savefig('cyl_vz.pdf')

if __name__=='__main__':
    main()
