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

from pycurb.analysis import loglog_power_fit as pfit


def main():
    dpath = '/home/upgp/jruebsam/simulations/feb16/week4/4_df_gc/'
    re = 100
    pr = 0.01
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
                vx = d.root.simdata.vx[-1, 4, 4, rs/2:(rs/2)+rs]

            z = np.linspace(0, 1, len(vx))
            thflow = -4*(z**2 - z)

            l2error = pa.l2_error(vx, exact=thflow)
            l2errorabs = pa.l2_error_abs(vx, exact=thflow)

            l2rel.append(l2error)
            l2abs.append(l2errorabs)
            res.append(rs)

        l2rel, l2abs, res = np.array(l2rel), np.array(l2abs), np.array(res)
        #np.save(path, np.column_stack((res, l2rel, l2abs)))
        #line, =ax.plot(res, l2rel, '^',  label=order, lw=1, ms=4, mew=0., alpha = 0.7)#, dashes=[2., 1.])
        ax.plot(res, l2rel, '^--',  label=order)


        if order == 'o4':
            fitfunc = lambda p, x: p[0]*x**p[1]
            errfunc = lambda p, x, y: fitfunc(p, x) - y
            p0 = [1., -2]
            p1, success = optimize.leastsq(errfunc, p0[:], args=(res, l2rel))
            p1, err = pfit(res, l2rel)

            xn = np.linspace(7, 200, 200)
            yn = fitfunc(p1, xn)
            line, = ax.plot(xn, yn, label='Fit: $ax^b$ : $b=%.3f\pm%f$' % (p1[1], err[0]))
        os.chdir(dpath)

    labels = ['relative'] #absolute identisch zu absolut
    os.chdir(plot_path)


    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel(r'gridpoints $N$')
    ax.set_ylabel(r'relative $l_2$-error')

    ax.set_xlim(5, 340)
    ax.set_ylim(1e-9, 1)

    #ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3),
    #       fancybox=True, shadow=True)

    plt.grid()
    plt.tight_layout()
    #plt.show()
    plt.legend()
    plt.savefig('relative_l2error.pdf')

if __name__=='__main__':
    main()



