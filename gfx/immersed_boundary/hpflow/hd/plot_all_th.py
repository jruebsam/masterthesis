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
    dpath = '/home/upgp/jruebsam/simulations/april15/week1/hpflow/gc/'
    modes = ['ip', 'dffrac', 'vpfrac']
    labels = ['Ip', 'DF-Vol.Frac.', 'VP-Vol.Frac.']

    re = 100.
    pmax = 4./re
    pr = 1./re
    rrel = 0.4
    lx, ly = 1/rrel, 1/rrel
    resf = np.linspace(16, 256., 256./16)
    resf = np.append(resf, 512)

    f, ax = style.newfig(1.)

    for mode, label in zip(modes, labels):
        on = 'o2'
        order = 1
        l2rel, l2abs, res = [], [], []
        for rs in reversed(resf):
            var_path = os.path.join(mode, on, 'res_%i' % rs)
            sim_path = os.path.join(os.path.dirname(__file__), "data", var_path)
            sim_path  = os.path.join(dpath, sim_path)

            with tb.open_file(sim_path +"/simulation.h5") as d:
                vz = d.root.simdata.vz[-1, :, :, 1]
                h = d.root.icdata.H[:,:, 1]

            dx = lx/rs
            z = np.linspace(0, 2.5-dx, rs)
            y, x = np.meshgrid(z, z)

            thflow =  (1  - ((x - 1.25)**2 + (y - 1.25)**2))*(1-h)
            thflow[thflow<0] = 0
            vz[thflow==0] = 0

            l2error = pa.l2_error(vz, exact=thflow)
            l2errorabs = pa.l2_error_abs(vz, exact=thflow)

            l2rel.append(l2error)
            l2abs.append(l2errorabs)
            res.append(rs)

            print l2error, mode, order

        l2rel, l2abs, res = np.array(l2rel), np.array(l2abs), np.array(res)
        lst = '--' if on=='o4' else ':'

        ms = 3 if not ((mode=='ipzero') and (on =='o2')) else 2

        ax.plot(res, l2rel, 'o'+lst, label = label + ' ' + on, ms=ms, mew=0)

    ax.legend(ncol = 3, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.3),
           fancybox=True, shadow=True)

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylim(4*1e-6, 2*1e-1)
    ax.set_xlim(15, 550)
    ax.set_xlabel(r'grid points N')
    ax.set_ylabel(r'rel. $l_2$-error')
    plt.subplots_adjust(top=0.8, bottom =0.15)

    plt.grid()
    plt.savefig('all.pdf')

if __name__=='__main__':
    main()
