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

from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def get_amp(series):
    n = len(series)/4
    data = series[3*n:]
    A = 0.5*(np.max(data)-np.min(data))
    return A

def main():
    dpaths = ['/home/upgp/jruebsam/simulations/mai16/week2/cone_wall/data/',
             '/home/upgp/jruebsam/simulations/mai16/week2/move_border/data/wall_0.500/']

    f, ax = style.newfig(0.8)
    cdir = os.getcwd()
    labels = ['Frustum', 'Cone']

    for dpath, label in zip(dpaths, labels):
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


        ax.plot(omgs, (a_vz), 'o-', ms=3, mew=0, lw=0.8,
                label=label)

       #plt.plot(omgs, a_vphi, 'ro--')
        #plt.plot(omgs, a_ekin, 'go--')
        os.chdir(cdir)


    from matplotlib import ticker
    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2,-3))

    #ax.set_ylim(0., 0.04)
    #ax.set_xlim(0.15, 2.05)
    ax.set_xlabel(r'$\omega$')
    ax.set_ylabel(r'$A\left(\left<v_z^2\right>_V\right)$')
    ax.legend(ncol = 3, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.12),
           fancybox=True, shadow=True)

    ax.yaxis.set_major_formatter(formatter)

    ax.grid(True)
    plt.subplots_adjust(top=0.9, bottom =0.15)
    plt.savefig('experiment.pdf')

if __name__=='__main__':
    main()
