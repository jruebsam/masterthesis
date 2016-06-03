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
    dpath = '/home/upgp/jruebsam/simulations/april16/week1/hpflow/long/'
    fs = style.figsize(0.9)#, 0.5)
    f, axes = plt.subplots(2, 3, figsize=fs)

    print fs

    modes = ['df', 'dffrac',  'vp',\
             'vpfrac', 'ip', 'ipzero' ]
    labels = ['DF', 'DF-VF.', 'VP', 'VP-VF.', 'IP', 'IP+DF']

    re = 100.
    pmax = 4./re

    pr = 1./re
    rrel = 0.4
    lx, ly = 1/rrel, 1/rrel

    rs = 96


    for label, method, ax  in zip(labels, modes, axes.flatten()):

        on = 'o4'

        var_path = os.path.join(method, on)
        sim_path = os.path.join(dpath, os.path.dirname(__file__), "data", var_path)

        with tb.open_file(sim_path +"/simulation.h5") as d:
            rho = d.root.simdata.rho[-1, :, :, 1]

        cax = ax.imshow(rho, interpolation='nearest')

        plt.sca(ax)
        c = f.colorbar(cax)#, pad=0., shrink=0.8, label=r'$\rho$')#, format='%.3g')
        c.formatter.set_powerlimits((0, 0))
        c.update_ticks()

        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])

        ax.set_title('{} {}'.format(label, 'FD4'), y=1.08)

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05)
    plt.tight_layout()
    plt.savefig('rho.pdf')


if __name__=='__main__':
    main()
