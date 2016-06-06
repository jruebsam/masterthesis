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
    path = '/home/upgp/jruebsam/simulations/april16/week1/tcflow/gc/data'
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

    f, ax = style.newfig(0.4, 1.)

    d = tb.open_file(path + '/ip/o2/res_128/simulation.h5')
    vx = d.root.simdata.vx[-1, :, :, 4]
    vy = d.root.simdata.vy[-1, :, :, 4]
    h = d.root.icdata.H[:,:, 1]
    v1 = np.sqrt(vx**2 + vy**2)*(1 - h)
    d.close()

    d = tb.open_file(path  + '/ipzero/o2/res_128/simulation.h5')
    vx = d.root.simdata.vx[-1, :, :, 4]
    vy = d.root.simdata.vy[-1, :, :, 4]
    h = d.root.icdata.H[:,:, 1]
    v2 = np.sqrt(vx**2 + vy**2)*(1 - h)
    d.close()

    im = ax.imshow(np.abs(v1-v2), origin='lower', interpolation='nearest', extent=[0, 1, 0, 1])
    c = plt.colorbar(im)
    c.formatter.set_powerlimits((0, 0))
    c.update_ticks()

    #c.set_ticks([])

    ax.set_ylabel(r'$|\Delta v|$')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])

    #plt.subplots_adjust(top=0.7, bottom =0.15, left=0.2)

    plt.savefig('vzdiff.pdf')

if __name__=='__main__':
    main()
