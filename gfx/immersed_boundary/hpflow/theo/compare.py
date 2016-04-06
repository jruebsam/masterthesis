#import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from glob import glob
import tables as tb
import pycurb.analysis as pa
from scipy import stats
import itertools as it
from scipy import optimize

import pycurb as pc

def main():

    modes = list(it.product(['df', 'dffrac', 'dffrac_cutoff',
                             'vp', 'vpfrac', 'vpfrac_cutoff',
                             'ip', 'ipzero' ], [1, 0]))
    re = 100.
    pmax = 4./re

    pr = 1./re
    rrel = 0.4
    lx, ly = 1/rrel, 1/rrel

    resf = np.array([16, 32, 64, 128, 256])

    for method, order in modes:
        res, l2rel, l2abs = [], [], []
        on = 'o2' if order else 'o4'

        hd_varpath = os.path.join(method, on, 'res_%i' % 512)
        hd_simpath = os.path.join(os.path.dirname(__file__), "data", hd_varpath)

        with tb.open_file(hd_simpath +"/simulation.h5") as d:
            vx = d.root.simdata.vx[-1, :, :, 1]
            vy = d.root.simdata.vy[-1, :, :, 1]
            h = d.root.icdata.H[:,:, 1]

        dx = lx/512.
        z = np.linspace(0, 2.5-dx, 512)
        y, x = np.meshgrid(z, z)

        thflow =  (1  - ((x - lx/2.)**2 + (y - ly/2.)**2))*(1-h)
        thflow[thflow<0] = 0

        for rs in reversed(resf):

            var_path = os.path.join(method, on, 'res_%i' % rs)
            sim_path = os.path.join(os.path.dirname(__file__), "data", var_path)
            with tb.open_file(sim_path +"/simulation.h5") as d:
                vz = d.root.simdata.vz[-1, :, :, 1]
                h = d.root.icdata.H[:,:, 1]

            p =  pc.Parameter(sim_path+"/parameter.json")
            dim = pc.Dimension(p)

            vabs = vz*(1 - h)

            vth = pa.shrink_grid(vabs, large_array=thflow)

            plt.imshow(vth-vabs, interpolation='nearest')
            plt.title('{} {} {}'.format(rs, method, order))
            plt.colorbar()
            plt.show()
            """
            """

            l2error = pa.l2_error(vabs, exact=vth)
            l2errorabs = pa.l2_error_abs(vabs, exact=vth)

            l2rel.append(l2error)
            l2abs.append(l2errorabs)
            res.append(rs)
            print l2error, method, order
        l2rel, l2abs, res = np.array(l2rel), np.array(l2abs), np.array(res)
        plt.plot(res, l2rel, 'o--', label = method + on)

    plt.legend()
    plt.yscale('log')
    plt.xscale('log')

    plt.show()

if __name__=='__main__':
    main()
