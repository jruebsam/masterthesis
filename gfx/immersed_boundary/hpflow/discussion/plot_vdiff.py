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
    path = '/home/upgp/jruebsam/simulations/april16/week1/hpflow/gc/data'
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

    d = tb.open_file(path + '/ip/o4/res_128/gfx/00000020.h5')
    d2 = tb.open_file(path  + '/ipzero/o2/res_128/gfx/00000020.h5')

    vz1 = d.root.xy.vz[:]
    vz2 = d2.root.xy.vz[:]

    im = ax.imshow(np.abs(vz1-vz2), origin='lower', interpolation='nearest', extent=[0, 1, 0, 1])
    c = plt.colorbar(im)
    c.formatter.set_powerlimits((0, 0))
    c.update_ticks()

    #c.set_ticks([])

    ax.set_ylabel(r'|v_x^{\text{FD4}} - v_x^{\text{FD2}}|')
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])

    #plt.subplots_adjust(top=0.7, bottom =0.15, left=0.2)

    plt.savefig('vzdiff.pdf')
    d.close()
    d2.close()

if __name__=='__main__':
    main()
