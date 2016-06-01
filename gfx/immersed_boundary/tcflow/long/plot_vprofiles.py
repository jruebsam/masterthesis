import style
style.setup()

import pycurb as pc

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
    dpath = '/home/upgp/jruebsam/simulations/april16/week1/tcflow/long/old'
    fs = style.figsize(0.9)#, 0.5)
    f, axes = plt.subplots(2, 3, figsize=fs)

    print fs
    modes = ['df', 'dffrac',  'vp',\
             'vpfrac', 'ip', 'ipzero' ]
    labels = ['DF', 'DF-Vol.Frac.', 'VP', 'VP-Vol.Frac.', 'IP', 'IP+DF']

    ri, ro, omg  = 1., 2., 1.

    lx, ly = 5., 5.
    nu = ri/ro

    A = -omg*nu**2/(1-nu**2)
    B = omg*ri**2/(1-nu**2)
    rs = 96


    for label, method, ax  in zip(labels, modes, axes.flatten()):

        on = 'o4'

        var_path = os.path.join(method, on)
        sim_path = os.path.join(dpath,   var_path)

        with tb.open_file(sim_path +"/simulation.h5") as d:
            vx = d.root.simdata.vx[-1, :, :, 4]
            vy = d.root.simdata.vy[-1, :, :, 4]
            h = d.root.icdata.H[:,:, 1]

        v = np.sqrt(vx**2 + vy**2)*(1 - h)

        p =  pc.Parameter(sim_path+"/parameter.json")
        dim = pc.Dimension(p)
        x, y, z = dim.get_grid()
        x, y = x[:, :, 0], y[:, :, 0]
        r = np.sqrt((x - lx/2.)**2 + (y-ly/2.)**2)
        vth = A*r + B/r
        vth *=(1 -h)

        vabs = np.sqrt(vx**2 + vy**2)
        vabs*=(1 - h)

        cax = ax.imshow(np.abs(v-vth), interpolation='nearest')

        plt.sca(ax)
        c = f.colorbar(cax)#, pad=0., shrink=0.8, label=r'$\rho$')#, format='%.3g')
        c.formatter.set_powerlimits((0, 0))
        c.update_ticks()

        ax.axes.get_xaxis().set_ticks([])
        ax.axes.get_yaxis().set_ticks([])

        ax.set_title('{} {}'.format(label, on), y=1.08)

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05)
    plt.tight_layout()
    plt.savefig('vz_profiles.pdf')


if __name__=='__main__':
    main()
