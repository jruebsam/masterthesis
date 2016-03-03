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

def main():
    dpath = '/home/upgp/jruebsam/simulations/mar16/week1/5_sine_default/'
    paths = ['data/o2', 'data/o4']

    f, ax = style.newfig(0.45, hscale=1.5)
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

            dx = 1./rs
            z = np.linspace(0, 1-dx, len(vx))
            thflow = np.sin(4*np.pi*z)

            l2error = pa.l2_error(vx, exact=thflow)
            l2errorabs = pa.l2_error_abs(vx, exact=thflow)

            l2rel.append(l2error)
            l2abs.append(l2errorabs)
            res.append(rs)

        l2rel, l2abs, res = np.array(l2rel), np.array(l2abs), np.array(res)
        ax.plot(res, l2rel, '^--',  label=order)

        if order == 'o2':
            xn = np.linspace(7, 160, 200)
            b = (res <20)
        else:
            xn = np.linspace(7, 40, 200)
            b = (res <100)

        fitfunc = lambda p, x: p[0]*x**p[1]
        errfunc = lambda p, x, y: fitfunc(p, x) - y
        p0 = [1., -2]
        p1, success = optimize.leastsq(errfunc, p0[:], args=(res[b], l2rel[b]))

        yn = fitfunc(p1, xn)
        ax.plot(xn, yn, label='fit: $ax^b$ : $b=%.3f$ +- ?' % p1[1])
        os.chdir(dpath)

    labels = ['relative'] #absolute identisch zu absolut
    os.chdir(plot_path)

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel(r'gridpoints $N$')
    ax.set_ylabel(r'relative $l_2$-error')

    ax.set_xlim(4, 300)
    #ax.set_ylim(1e-10, 1e-1)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.55),
           fancybox=True, shadow=True, fontsize=7)

    plt.grid()
    plt.tight_layout()
    plt.subplots_adjust(top=0.7)
    #plt.show()
    plt.savefig('relative_l2error.pdf')

if __name__=='__main__':
    main()



