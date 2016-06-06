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
from scipy import optimize

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def main():
    #dpath = '/home/upgp/jruebsam/simulations/april16/week1/tcflow/gc/'
    dpath = '/home/upgp/jruebsam/simulations/june16/week1/tclong'

    modes = ['df', 'dffrac',  'vp', 'vpfrac', 'ip', 'ipzero']
    labels = ['DF', 'DF-VF', 'VP', 'VP-VF', 'IP', 'IP+DF']

    re = 100.
    pmax = 4./re
    pr = 1./re
    rrel = 0.4
    lx, ly = 1/rrel, 1/rrel

    rs = 96

    f, ax = style.newfig(0.5, 1.8)
    for on in ['o2', 'o4']:
        plt.gca().set_color_cycle(cmap)
        onn = 'FD2' if on=='o2' else 'FD4'
        for label, method  in zip(labels, modes):
            print method, on
            if ((method=='ipzero') and (on=='o4')):
                continue

            onn = 'FD2' if on=='o2' else 'FD4'
            var_path = os.path.join(method, on)
            sim_path = os.path.join(dpath, os.path.dirname(__file__), "data", var_path)
            d = np.genfromtxt(os.path.join(sim_path , '%s.ekin' % on))
            if on == 'o2':
                ax.plot(d[:, 0], d[:, 3], label=label+ ' ' + onn , lw=0.8)
            else:
                ax.plot(d[:, 0], d[:, 3], '--', label=label+ ' ' + onn , lw=0.8, dashes=(1, 2, 1, 2))

        ax.legend(ncol = 2, fontsize=8, loc='lower left', fancybox=True, shadow=True)

        plt.subplots_adjust(top=0.65, bottom =0.15, left=0.2)
        ax.legend(ncol = 2, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.6), labelspacing=0.2,
               fancybox=True, shadow=True)

        ax.set_xlabel('Total time')
        ax.set_ylabel(r'$\rho$')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.subplots_adjust(bottom =0.15)
    ax.set_xlim(0, 1200)

    plt.savefig('ts_all.pdf')#%s.pdf' % on)


if __name__=='__main__':
    main()
