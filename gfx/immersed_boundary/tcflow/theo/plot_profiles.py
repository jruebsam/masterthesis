import style
#style.setup()

import numpy as np
import pycurb as pc
import matplotlib.pyplot as plt
import os, sys
from glob import glob
import tables as tb
import pycurb.analysis as pa
from scipy import stats
import itertools as it

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def main():
    dpath = '/home/upgp/jruebsam/simulations/april15/week1/tcflow/gc/'
    #labels = ['IP', 'IP + DF']

    modes = list(it.product(['df', 'dffrac', 'dffrac_cutoff',
                             'vp', 'vpfrac', 'vpfrac_cutoff',
                             'ip', 'ipzero' ], [1, 0]))
    ri, ro, omg  = 1., 2., 1.

    lx, ly = 5., 5.
    nu = ri/ro

    A = -omg*nu**2/(1-nu**2)
    B = omg*ri**2/(1-nu**2)

    resf = np.linspace(16, 256., 256./16)
    resf = np.append(resf, 512)
    f, ax = style.newfig(1.)

    #for mode, label in zip(modes, labels):
    for mode, order in modes:
        for order in [0, 1]:
            for rs in reversed(resf):
                on = 'o2' if order else 'o4'
                var_path = os.path.join(mode, on, 'res_%i' % rs)
                sim_path = os.path.join(os.path.dirname(__file__), "data", var_path)
                sim_path  = os.path.join(dpath, sim_path)

                with tb.open_file(sim_path +"/simulation.h5") as d:
                    vx = d.root.simdata.vx[-1, :, :, 1]
                    vy = d.root.simdata.vy[-1, :, :, 1]
                    h = d.root.icdata.H[:,:, 1]
                b = (h==1)

                p =  pc.Parameter(sim_path+"/parameter.json")
                dim = pc.Dimension(p)
                x, y, z = dim.get_grid()
                x, y = x[:, :, 0], y[:, :, 0]
                r = np.sqrt((x - lx/2.)**2 + (y-ly/2.)**2)
                vth = A*r + B/r
                vth[b] = 0

                vabs = np.sqrt(vx**2 + vy**2)
                vabs[b] = 0
                if rs == 128:
                    plt.imshow(vth - vabs)
                    plt.title("{} {}".format(mode, order))
                    plt.colorbar()
                    plt.show()


    #plt.savefig('ip.pdf')


if __name__=='__main__':
    main()
