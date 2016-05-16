import style
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
    dpath = '/home/upgp/jruebsam/simulations/april16/week2/cylinder_series/'

    labels = ['DF', 'DF-Vol.Frac.']

    f, ax = style.newfig(1.)

    modes = list(it.product(['df', 'vp', 'dffrac', 'vpfrac'], [1, 0]))

    for method, order in modes:
        on = 'o2' if order else 'o4'
        a_ekin, a_vz, a_vphi = [], [], []
        omgs = []
        omgfs = np.arange(0.2, 2.1, 0.1)
        omgs = omgfs

        for omgf in [0.8]:
            var_path = os.path.join(method, on, 'omg_{}'.format(omgf))
            sim_path = os.path.join(dpath, "data", var_path)

            dp = os.path.join(sim_path, '.'.join([sim_path.split('/')[-1], 'ekin']))
            simpath = dp
            try:
                data = np.genfromtxt(dp)
                time = data[:, 0]
                ekin = data[:, 1]
                vz   = data[:, -3]
                vphi = data[:, -1]
            except:
                pass

        mks = markers.next()
        col = cc.next()
        ax.plot(time, vz, color=col, ms=4, mew=0, lw=0.7, alpha =1.,
                label=method+'/'+on)

    ax.set_ylim(0., 0.0005)
    ax.set_xlim(80, 100)
    ax.set_xlabel(r'time')
    ax.set_ylabel(r'$v_z^2$')
    plt.legend(ncol = 3, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.3),
           fancybox=True, shadow=True)

    plt.subplots_adjust(top=0.8, bottom =0.15)
    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2,-3))
    ax.yaxis.set_major_formatter(formatter)

    ax.grid(True)
    plt.savefig('cyl_vz.pdf')

if __name__=='__main__':
    main()
