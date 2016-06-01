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
    modes = ['dffrac', 'vpfrac', 'ip', 'ip']
    labels = ['DF-Vol.Frac', 'VP-Vol.Frac', 'IP' , 'IP']
    orders = [1, 1, 1, 0]

    re = 100.
    pmax = 4./re
    pr = 1./re
    rrel = 0.4
    lx, ly = 1/rrel, 1/rrel
    resf = np.linspace(16, 256., 256./16)
    resf = np.append(resf, 512)

    f, ax = style.newfig(0.5, 1.7)

    i=3
    order = 'o4'
    on = order
    N = rs = 256
    method = modes[1]


    var_path = os.path.join(method, on)
    sim_path = os.path.join(dpath, os.path.dirname(__file__), "data", var_path, 'simulation.h5')

    with tb.open_file(sim_path, 'r') as d:
        rho = d.root.simdata.rho[-1, :, :, 1]


    im = ax.imshow(rho.T, origin='lower', interpolation='nearest', extent=[0, 1, 0, 1])
    c = plt.colorbar(im)
    c.formatter.set_powerlimits((0, 0))
    c.update_ticks()

    #c.set_ticks([])
    c.set_label(r'$\rho(x, y, z=0.5)$')

    ax.set_xlabel('y')
    ax.set_ylabel('z')
    ax.set_title(r'DF-Vol.Frac. o2, $N=256$')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])

    plt.subplots_adjust(top=0.7, bottom =0.15, left=0.2)

    plt.savefig('example.pdf')

if __name__=='__main__':
    main()
