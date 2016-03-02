import style
style.setup()

import numpy as np
import pycurb.analysis as pa
import tables as tb
import os
from scipy import optimize

import matplotlib.pyplot as plt

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def flow(x, pr, h1, h2, pmax):
    return -1/(2*pr)*pmax*(x**2 - x*(h1 + h2) + h1*h2)

def main():
    dpath = '/home/upgp/jruebsam/simulations/feb16/week4/1_default/'
    pmax, h1, h2, re = 10., 0, 1, 500
    pr = np.sqrt(0.125*pmax/re)
    paths = ['data/o2', 'data/o4']

    f, ax = style.newfig(0.8)
    plot_path = os.getcwd()
    os.chdir(dpath)

    for path in paths:
        order = path.split('/')[-1]
        print "Reading path %s " % path
        os.chdir(path)
        sim_paths = sorted(os.listdir(os.getcwd()), key=lambda x: int(x.split('_')[-1]))

        res, l2rel, l2abs = [], [], []
        for sp in sim_paths:
            rs = int(sp.split('_')[-1])

            with tb.open_file(os.path.join(sp, "simulation.h5")) as d:
                vx = d.root.simdata.vx[-1, 8,8,:]
            try:
                z = np.linspace(0, 1, len(vx))
                thflow = -4*(z**2 - z)

                l2error = pa.l2_error(vx, exact=thflow)
                l2errorabs = pa.l2_error_abs(vx, exact=thflow)

                l2rel.append(l2error)
                l2abs.append(l2errorabs)
                res.append(rs)
            except:
                print 'TADAAA'

        l2rel, l2abs, res = np.array(l2rel), np.array(l2abs), np.array(res)
        #np.save(path, np.column_stack((res, l2rel, l2abs)))
        ax.plot(res, l2rel, '^--',  label=order)


        if order == 'o4':
            fitfunc = lambda p, x: p[0]*x**p[1]
            errfunc = lambda p, x, y: fitfunc(p, x) - y
            p0 = [1., -2]
            p1, success = optimize.leastsq(errfunc, p0[:], args=(res, l2rel))

            xn = np.linspace(7, 160, 200)
            yn = fitfunc(p1, xn)
            ax.plot(xn, yn, label='fit: $ax^b$ : $b=%.3f$ +- ?' % p1[1])
        os.chdir(dpath)

    labels = ['relative'] #absolute identisch zu absolut
    os.chdir(plot_path)


    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel(r'gridpoints $N$')
    ax.set_ylabel(r'relative $l_2$-error')

    ax.set_xlim(5, 300)
    ax.set_ylim(1e-10, 1e-1)

    plt.legend()
    plt.grid()
    plt.tight_layout()
    #plt.show()
    plt.savefig('relative_l2error.pdf')

if __name__=='__main__':
    main()



