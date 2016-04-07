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
    dpath = '/home/upgp/jruebsam/simulations/april15/week1/hpflow/gc/'
    modes = ['dffrac', 'vpfrac', 'ip', 'ip']
    print modes

    labels = ['DF-Vol.Frac', 'VP-Vol.Frac', 'IP' , 'IP']
    orders = [1, 1, 1, 0]

    re = 100.
    pmax = 4./re
    pr = 1./re
    rrel = 0.4
    lx, ly = 1/rrel, 1/rrel
    resf = np.linspace(16, 256., 256./16)
    resf = np.append(resf, 512)

    f, (ax, ax2) = plt.subplots(1, 2, figsize = style.figsize(1, hscale=0.5))

    for mode, label, order in zip(modes, labels, orders):
        l2rel, l2abs, res = [], [], []
        on = 'o2' if order else 'o4'

        hd_varpath = os.path.join(mode, on, 'res_%i' % 512)
        hd_simpath = os.path.join(dpath, os.path.dirname(__file__), "data", hd_varpath)

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
            var_path = os.path.join(mode, on, 'res_%i' % rs)
            sim_path = os.path.join(os.path.dirname(__file__), "data", var_path)
            sim_path  = os.path.join(dpath, sim_path)

            with tb.open_file(sim_path +"/simulation.h5") as d:
                vz = d.root.simdata.vz[-1, :, :, 1]
                h = d.root.icdata.H[:,:, 1]

            dx = lx/rs
            z = np.linspace(0, 2.5-dx, rs)
            y, x = np.meshgrid(z, z)

            thflow =  (1  - ((x - 1.25)**2 + (y - 1.25)**2))*(1-h)
            thflow[thflow<0] = 0
            vz[thflow==0] = 0

            if ((rs==256) and (mode=='dffrac')):
                cax = ax2.imshow((vz -thflow).T, interpolation='nearest', origin='lower', extent=[0, 1, 0, 1])
                cbar = f.colorbar(cax, pad = 0.1, shrink=0.9)
                ax2.set_xlabel('x')
                ax2.set_ylabel('y')
                ax2.set_title('(b) DF-Vol.Frac N=256')

            l2error = pa.l2_error(vz, exact=thflow)
            l2errorabs = pa.l2_error_abs(vz, exact=thflow)

            l2rel.append(l2error)
            l2abs.append(l2errorabs)
            res.append(rs)

            print l2error, mode, order

        l2rel, l2abs, res = np.array(l2rel), np.array(l2abs), np.array(res)
        lst = '--' if on=='o4' else ':'

        ms = 3 if not ((mode=='ipzero') and (on =='o2')) else 2

        popt, perr = pa.loglog_power_fit(res, l2rel)#, p0=[1., -2.])
        xn = np.linspace(16, 512, 100)
        yn = popt[0]*xn**popt[1]
        ax.plot(res, l2rel, 'o'+lst, label = label+ ' ' + on + ' (Fit:$b=%.3f\pm %.3f$'\
                                        % (popt[1], perr[1]), ms=3, mew=0)

    ax.legend(ncol = 3, fontsize=6, loc='upper center', bbox_to_anchor=(1.1, 1.3),
           fancybox=True, shadow=True)

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_title('(a) GC-Study')
    #ax.set_ylim(4*1e-6, 2*1e-1)
    #ax.set_xlim(15, 550)
    ax.set_xlabel(r'grid points N')
    ax.set_ylabel(r'rel. $l_2$-error')
    plt.subplots_adjust(top=0.8, bottom =0.15)

    plt.grid()
    plt.savefig('all.pdf')

if __name__=='__main__':
    main()