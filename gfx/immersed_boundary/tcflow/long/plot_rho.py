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
    dpath = '/home/upgp/jruebsam/simulations/april16/week1/tcflow/gc/'

    modes = ['df', 'dffrac',  'vp', 'vpfrac', 'ip']
    labels = ['DF', 'DF-Vol.Frac.', 'VP', 'VP-Vol.Frac.', 'IP']

    re = 100.
    pmax = 4./re

    pr = 1./re
    rrel = 0.4
    lx, ly = 1/rrel, 1/rrel

    rs = 96

    for on in ['o2', 'o4']

        onn = 'FD2' if on == 'o2' else 'FD4'

        f, ax = style.newfig(0.8)
        for label, method  in zip(labels, modes):

            var_path = os.path.join(method, on, 'res_96')
            sim_path = os.path.join(dpath, os.path.dirname(__file__), "data", var_path)
            d = np.genfromtxt(os.path.join(sim_path , 'res96.ekin'))

            ax.plot(d[:, 0], d[:, 3], label=label+ ' ' + onn )


        ax.legend(ncol = 2, fontsize=8, loc='lower left', fancybox=True, shadow=True)

        ax.set_xlabel('Total time')
        ax.set_ylabel(r'$\rho$')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        plt.subplots_adjust(bottom =0.15)

        plt.savefig('ts_%s.pdf' % on)


if __name__=='__main__':
    main()
