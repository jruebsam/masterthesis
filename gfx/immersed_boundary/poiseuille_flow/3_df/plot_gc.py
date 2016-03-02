import style
style.setup()

import numpy as np
import matplotlib.pyplot as plt
import os, sys
from glob import glob
import tables as tb
import pycurb.analysis as pa
from scipy import stats
import itertools
from scipy import optimize

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def flow(x, h1, h2):
    return -4*(x**2 - x*(h1 + h2) + h1*h2)

def main():
    plot_dir = os.getcwd()
    cdir = '/home/upgp/jruebsam/simulations/feb16/week4/4_df_gc/'
    os.chdir(cdir)

    marker = itertools.cycle(('^', '*', 'x', 'o', 'D'))
    pmax, h1, h2, re = 10., 0, 1, 10.0
    pr = np.sqrt(0.125*pmax/re)
    paths = glob('data/*o*')

    for path in paths:
        print "Reading path %s " % path
        os.chdir(os.path.join(path))#, 'data'))
        sim_paths = sorted(os.listdir(os.getcwd()), key=lambda x: int(x.split('_')[-1]))

        res, l2rel, l2abs = [], [], []
        order = path.split('/')[-1]

        for sp in sim_paths:
            cp = os.getcwd()
            os.chdir(sp)
            rs = int(sp.split('_')[-1])

            with tb.open_file("simulation.h5") as d:
                vx = d.root.simdata.vx[-1, 4, 4, rs/2:(rs/2)+rs]

            l = (len(vx) - rs)/2.
            vx = vx[l:l+rs]
            z = np.linspace(0, 1, len(vx))

            thflow = flow(z, 0, 1)

            """
            plt.plot(thflow, 'r:')
            plt.plot(vx, 'bo-')
            plt.show()
            """

            l2error = pa.l2_error(vx, exact=thflow)
            l2errorabs = pa.l2_error_abs(vx, exact=thflow)

            l2rel.append(l2error)
            l2abs.append(l2errorabs)
            res.append(rs)
            os.chdir(cp)

        l2rel, l2abs, res = np.array(l2rel), np.array(l2abs), np.array(res)
        os.chdir(cdir)
        plt.plot(res, l2rel, marker.next()+'--', label = order)

        if order == 'o4':
            fitfunc = lambda p, x: p[0]*x**p[1]
            errfunc = lambda p, x, y: fitfunc(p, x) - y
            p0 = [1., -2]
            p1, success = optimize.leastsq(errfunc, p0[:], args=(res, l2rel))
            xn = np.linspace(7, 300, 200)
            yn = fitfunc(p1, xn)

            plt.plot(xn, yn, label='fit: $ax^b$ : $b=%.3f$ +- ?' % p1[1])

    os.chdir(plot_dir)
    plt.legend()
    plt.xlim(7, 350)
    plt.ylim(5*1e-9, 2)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Gridpoints N')
    plt.ylabel('$l_2$-rel. error')
    #plt.show()
    plt.savefig('df_convergence.pdf')

if __name__=='__main__':
    main()
