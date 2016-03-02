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

def flow(x, h1, h2):
    return -4*(x**2 - x*(h1 + h2) + h1*h2)

def main():
    nus = 0.1**np.arange(5)
    nus = np.append(nus, 5*0.1**np.arange(5))
    nus = np.array(sorted(nus))

    # Using contourf to provide my colorbar info, then clearing the figure
    Z = [[0,0],[0,0]]
    levels = np.arange(100, 525, 25)

    CS1 = plt.contourf(Z, levels, cmap='jet')
    CS2 = plt.contourf(Z, np.arange(len(nus)), cmap='jet')
    plt.clf()
    f, (ax1, ax2) = plt.subplots(1, 2,  figsize=style.figsize(0.9))

    #= style.newfig(0.9)


    plot_path = os.getcwd()
    dpath = '/home/upgp/jruebsam/simulations/feb16/week4/2_vp_error_nu_re'
    os.chdir(dpath)

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
            re = int(sp.split('_')[-1])

            with tb.open_file("simulation.h5") as d:
                vx = d.root.simdata.vx[-1, 4, 4, rs/2:(rs/2)+rs]

            z = np.linspace(0, 1, len(vx))
            thflow = flow(z, 0, 1)

            l2error = pa.l2_error(vx, exact=thflow)
            l2errorabs = pa.l2_error_abs(vx, exact=thflow)

            l2rel.append(l2error)
            l2abs.append(l2abs)

            res.append(re)
            nus.append(nu)
            os.chdir(cp)
        os.chdir(cdir)
    os.chdir(plot_path)

    allnus = sorted(list(set(list(nus))))
    allres = sorted(list(set(list(res))))
    values = range(len(allres))

    res = np.array(res)
    l2rel = np.array(l2rel)
    nus = np.array(nus)

    ######
    #PLOT1
    plt.sca(ax1)
    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=len(allres))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    for idx, re in enumerate(allres):
        b = (res == re)
        colorVal = scalarMap.to_rgba(values[idx])

        ax1.plot(nus[b], l2rel[b], 'o', color=colorVal, label=r'$Re=%i$' % re, ms=5, mew=0)
    #FIT
    b = (res == 500) & (nus<1e-2)
    fitfunc = lambda p, x: p[0]*x**p[1]
    errfunc = lambda p, x, y: fitfunc(p, x) - y
    p0 = [1., 1.]
    p1, success = optimize.leastsq(errfunc, p0[:], args=(nus[b], l2rel[b]))

    xn = np.linspace(1e-5, 1e-2)
    yn = fitfunc(p1, xn)
    fit, = ax1.plot(xn, yn, '--', lw=1)
    legend_fit = plt.legend([fit],['fit: $ax^b$ : $b=%.3f$ +- ?' % p1[1]], loc=4, fontsize=7)
    plt.gca().add_artist(legend_fit)
    ax1.set_xlabel(r'$J$')
    ax1.set_ylabel('$l_2$-rel. error')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlim(0.8*1e-4, 8)
    ax1.set_ylim(0.8*1e-5, 2)

    ######
    #PLOT2
    plt.sca(ax2)
    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=len(allnus))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    for idx, nu in enumerate(allnus):
        b = (nus == nu)
        colorVal = scalarMap.to_rgba(values[idx])
        ax2.plot(res[b], l2rel[b], 'o', color=colorVal, ms=5, mew=0)

    #FIT
    b = (nus == 0.0001)
    fitfunc = lambda p, x: p[0]*x**p[1]
    errfunc = lambda p, x, y: fitfunc(p, x) - y
    p0 = [-0.1, -0.1]
    p1, success = optimize.leastsq(errfunc, p0[:], args=(res[b], l2rel[b]))
    print success

    xn = np.linspace(100, 500, 1001)
    yn = fitfunc(p1, xn)
    fit, = ax2.plot(xn, yn, 'r--', lw=1)
    legend_fit = plt.legend([fit],['fit: $ax^b$ : $b=%.3f$ +- ?' % p1[1]], loc=3, fontsize=7)
    plt.gca().add_artist(legend_fit)

    ax2.set_xlabel(r'$Re$')
    ax2.set_ylabel('$l_2$-rel. error')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlim(90, 550)
    ax2.set_ylim(3*1e-6, 2)

    ##ALLPLOTS
    #plt.subplots_adjust(right=0.84, bottom=0.13)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),
    #                  ncol=1, fancybox=True, shadow=True, fontsize=7)

    plt.sca(ax1)
    cb1 = plt.colorbar(CS1, pad=0.)
    plt.sca(ax2)
    cb2 = plt.colorbar(CS2, pad=0.)
    cb2.set_ticklabels(["%0.0e" % x for x in allnus])#(np.arange(len(nus)), nus)

    cb1.set_label(r'Re')
    cb2.set_label(r'J')

    plt.tight_layout()
    plt.savefig('vp_error.pdf')
    #plt.show()

if __name__=='__main__':
    main()
