import style
style.setup()

import numpy as np
import pycurb.analysis as pa
import matplotlib.pyplot as plt
import pickle
import os
import tables as tb
from glob import glob
import matplotlib.colors as colors
import matplotlib.cm as cmx

from scipy import optimize
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def flow(x, pr, h1, h2, pmax):
    return -1/(2*pr)*pmax*(x**2 - x*(h1 + h2) + h1*h2)

def main():
    plot_path = os.getcwd()
    dpath = '/home/upgp/jruebsam/simulations/feb16/week2/2_vp_error_nu_re'
    os.chdir(dpath)

    pmax, h1, h2, re = 10., 0, 1, 10.0
    rs =64

    paths = sorted(glob('data/*/*o2*'), key=lambda x: float((x.split('/')[1]).split('_')[-1]))
    cdir = os.getcwd()

    res, l2rel, l2abs = [], [], []
    nus = []

    for path in paths:
        print "Reading path %s " % path

        os.chdir(os.path.join(path))
        sim_paths = sorted(os.listdir(os.getcwd()), key=lambda x: int(x.split('_')[-1]))

        nu = float((path.split('/')[1]).split('_')[-1])

        for sp in sim_paths:
            cp = os.getcwd()
            os.chdir(sp)

            with tb.open_file("simulation.h5") as d:
                vx = d.root.simdata.vx[-1, 4, 4, rs/2:(rs/2)+rs]

            re = float(sp.split('_')[-1])
            pr = np.sqrt(0.125*pmax/re)

            z = np.linspace(0, 1, len(vx))
            thflow = flow(z, pr, 0, 1, pmax)

            l2error = pa.l2_error(vx, exact=thflow)
            l2errorabs = pa.l2_error_abs(vx, exact=thflow)

            l2rel.append(l2error)
            l2abs.append(l2abs)

            res.append(re)
            nus.append(nu)

            os.chdir(cp)

        os.chdir(cdir)
    os.chdir(plot_path)
    f, ax = style.newfig(0.9)

    allnus = sorted(list(set(list(nus))))
    allres = sorted(list(set(list(res))))
    values = range(len(allnus))

    res = np.array(res)
    l2rel = np.array(l2rel)
    nus = np.array(nus)

    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=len(allnus))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    for idx, re in enumerate(allres):
        b = (res == re)
        colorVal = scalarMap.to_rgba(values[idx])

        ax.plot(nus[b], l2rel[b], 'o', color=colorVal, label=r'$Re=%i$' % re, ms=5, mew=0)
    #FIT
    b = (res == 500) & (nus<1e-2)
    fitfunc = lambda p, x: p[0]*x**p[1]
    errfunc = lambda p, x, y: fitfunc(p, x) - y
    p0 = [1., 1.]
    p1, success = optimize.leastsq(errfunc, p0[:], args=(nus[b], l2rel[b]))

    xn = np.linspace(1e-5, 1e-2)
    yn = fitfunc(p1, xn)
    fit, = ax.plot(xn, yn, '--', lw=1)
    legend_fit = plt.legend([fit],['fit: $ax^b$ : $b=%.3f$ +- ?' % p1[1]], loc=4)
    plt.gca().add_artist(legend_fit)

    ax.set_xlabel(r'$\nu$')

    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.xlabel(r'Damping $\nu$')
    plt.ylabel('$l_2$-rel. error')
    plt.xlim(0.8*1e-5, 1e0)
    plt.subplots_adjust(right=0.84, bottom=0.13)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                      ncol=1, fancybox=True, shadow=True, fontsize=7)


    plt.savefig('vp_error.pdf')
    #plt.show()

if __name__=='__main__':
    main()
