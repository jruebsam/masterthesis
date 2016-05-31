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
    dpath = '/home/upgp/jruebsam/simulations/april16/week1/hpflow/gc/'
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

    i=0
    order = 'o4'
    N = rs = 256

    hd_varpath = os.path.join(modes[i], order, 'res_%i' % 512)
    hd_simpath = os.path.join(dpath, "data", hd_varpath, 'simulation.h5')

    with tb.open_file(hd_simpath, 'r') as d:
        vx = d.root.simdata.vx[-1, :, :, 1]
        vy = d.root.simdata.vy[-1, :, :, 1]
        h = d.root.icdata.H[:,:, 1]
    dx = lx/512.
    z = np.linspace(0, 2.5-dx, 512)
    y, x = np.meshgrid(z, z)
    thflow =  (1  - ((x - lx/2.)**2 + (y - ly/2.)**2))*(1-h)
    thflow[thflow<0] = 0


    fpath = os.path.join(dpath, 'data', modes[i], order,  ('res_%i' % N), 'simulation.h5')

    with tb.open_file(fpath, 'r') as d:
        vz = d.root.simdata.vz[-1, :, :, 1]
        h = d.root.icdata.H[:,:, 1]

    dx = lx/rs
    z = np.linspace(0, 2.5-dx, rs)
    y, x = np.meshgrid(z, z)

    thflow =  (1  - ((x - 1.25)**2 + (y - 1.25)**2))*(1-h)
    thflow[thflow<0] = 0
    vz[thflow==0] = 0

    im = ax.imshow(np.abs(vz -thflow).T, origin='lower', interpolation='nearest', extent=[0, 1, 0, 1])
    c = plt.colorbar(im)

    c.set_ticks([])
    c.set_label(r'$\propto v_\mathrm{x} - v_{\mathrm{th}}$')

    ax.set_xlabel('y')
    ax.set_ylabel('z')
    ax.set_title(r'DF-Vol.Frac. o2, $N=256$')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])

    plt.subplots_adjust(top=0.7, bottom =0.15, left=0.2)

    plt.savefig('example.pdf')

if __name__=='__main__':
    main()
