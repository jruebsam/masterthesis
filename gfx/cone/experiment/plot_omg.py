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
    dpaths = ['/home/upgp/jruebsam/simulations/mai16/week2/cone_wall/data/',
             '/home/upgp/jruebsam/simulations/mai16/week2/move_border/data/wall_0.500/']

    f, ax = style.newfig(1., 0.7)
    cdir = os.getcwd()

    for dpath in dpaths:
        os.chdir(dpath)

        a_ekin, a_vz, a_vphi = [], [], []
        omgs = []
        simpathes =  glob('*/*.ekin')

        for i, simpath in enumerate(sorted(simpathes)):
            omg = float((simpath.split('/')[-2]).split('_')[1])
            dp = simpath

            data = np.genfromtxt(dp)
            time = data[:, 0]
            ekin = data[:, 1]
            vz   = data[:, -3]
            vphi = data[:, -1]
            #ax.plot(time, vz, label=simpath)
            a_ekin.append(get_amp(ekin))
            a_vz.append(get_amp(vz))
            a_vphi.append(get_amp(vphi))
            omgs.append(omg)
            #plt.plot(time, vz, label=simpath.split('/')[-1])

        a_vz = np.array(a_vz)
        print a_vz

        if dpath == dpaths[0]:
            a_vz/=0.16

        mks = markers.next()
        col = cc.next()

        ax.plot(omgs, (a_vz), mks+'--', color=col, ms=4, mew=0, lw=0.5,
                label=1)

       #plt.plot(omgs, a_vphi, 'ro--')
        #plt.plot(omgs, a_ekin, 'go--')
        os.chdir(cdir)

    plt.subplots_adjust(top=0.8, bottom =0.15)

    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2,-3))

    #ax.set_ylim(0., 0.04)
    #ax.set_xlim(0.15, 2.05)
    ax.set_xlabel(r'$\omega$')
    ax.set_ylabel(r'$v_z^2$')
    ax.legend(ncol = 3, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.3),
           fancybox=True, shadow=True)

    ax.yaxis.set_major_formatter(formatter)

    ax.grid(True)
    plt.savefig('experiment.pdf')

if __name__=='__main__':
    main()
