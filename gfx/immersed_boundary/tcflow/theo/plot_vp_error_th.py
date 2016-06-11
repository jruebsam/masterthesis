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
    dpath = '/home/upgp/jruebsam/simulations/april16/week1/tcflow/gc/'
    modes = ['vp', 'vpfrac']
    labels = ['VP', 'VP-VF.']



    ri, ro, omg  = 1., 2., 1.

    lx, ly = 5., 5.
    nu = ri/ro

    A = -omg*nu**2/(1-nu**2)
    B = omg*ri**2/(1-nu**2)

    resf = np.linspace(16, 256., 256./16)
    resf = np.append(resf, 512)
    f, ax = style.newfig(0.5, 1.7)

    for mode, label in zip(modes, labels):
        for order in [0, 1]:
            l2rel, l2abs, res = [], [], []
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


                l2error = pa.l2_error(vabs, exact=vth)
                l2errorabs = pa.l2_error_abs(vabs, exact=vth)

                l2rel.append(l2error)
                l2abs.append(l2errorabs)
                res.append(rs)

                print l2error, mode, order

            l2rel, l2abs, res = np.array(l2rel), np.array(l2abs), np.array(res)
            lst = '--' if on=='o4' else ':'

            #f label=='VP' and on = 'o4':
            #   b = res<130
            #   popt, perr = pa.loglog_power_fit(res[b], l2rel[b])#, p0=[1., -2.])
            #else:
            popt, perr = pa.loglog_power_fit(res, l2rel)#, p0=[1., -2.])
            xn = np.linspace(16, 512, 100)
            yn = popt[0]*xn**popt[1]
            #if (mode=='vpfrac') and (on =='o2'):
            #    ax.plot(xn, yn, 'k--', lw=0.5, label='Fit for VP-Vol.Frac. o2 $\propto N^b$' % popt[1])


            onn = 'FD2' if order else 'FD4'
            lb = label+ ' ' + onn + (':$\lambda=%.2f\pm%.2f$'  % (popt[1], perr[1]))
            ax.plot(res, l2rel, 'o-', ms=3, lw=0.8, mew = 0, label = lb)

    plt.subplots_adjust(top=0.7, bottom =0.15, left=0.2)
    ax.legend(ncol = 1, fontsize=8, loc='upper center', bbox_to_anchor=(0.5, 1.5),
           fancybox=True, shadow=True)

    ax.set_yscale('log')
    ax.set_xscale('log')
    #ax.set_ylim(1e-4, 2*1e-1)
    ax.set_xlim(15, 550)
    ax.set_xlabel(r'grid points N')
    ax.set_ylabel(r'rel. $l_2$-error $\epsilon$')

    plt.grid()
    plt.savefig('vp.pdf')

if __name__=='__main__':
    main()
