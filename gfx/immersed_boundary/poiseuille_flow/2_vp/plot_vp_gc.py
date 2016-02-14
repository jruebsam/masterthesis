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

def flow(x, pr, h1, h2, pmax):
    return -1/(2*pr)*pmax*(x**2 - x*(h1 + h2) + h1*h2)

def main():
    f = plt.figure(figsize=style.figsize(0.9))

    plot_dir = os.getcwd()
    cdir = '/home/upgp/jruebsam/simulations/feb16/week2/3_vp_gc/'
    os.chdir(cdir)

    marker = itertools.cycle(('^', '*', 'x', 'o', 'D'))

    pmax, h1, h2, re = 10., 0, 1, 10.0
    pr = np.sqrt(0.125*pmax/re)

    len_nus = len(0.1**np.arange(1, 6))*2

    cm_o2 = plt.get_cmap('Blues')
    cm_o4 = plt.get_cmap('Reds')

    o2gen = (cm_o2((i*1.0 + 5 )/(len_nus + 5)) for i in range(len_nus))
    o4gen = (cm_o4((i*1.0 + 5)/(len_nus + 5)) for i in range(len_nus))

    path_o2 = sorted(glob('data/*/*o2*'), key=lambda x: \
            float((x.split('/')[1]).split('_')[-1]))[::-1]

    path_o4 = sorted(glob('data/*/*o4*'), key=lambda x: \
            float((x.split('/')[1]).split('_')[-1]))[::-1]

    paths = path_o2
    paths.extend(path_o4)

    for path in paths:
        print "Reading path %s " % path

        so = path.split('/')
        print so
        nu = float(so[1].split('_')[-1])
        order = int(so[2][1:])
        print nu, order

        gen = o2gen if order == 2 else o4gen
        mark = 'o--' if order == 2 else '*--'

        os.chdir(os.path.join(path))#, 'data'))
        sim_paths = sorted(os.listdir(os.getcwd()), key=lambda x: int(x.split('_')[-1]))

        res, l2rel, l2abs = [], [], []
        pes = []

        for sp in sim_paths:
            cp = os.getcwd()
            os.chdir(sp)
            rs = int(sp.split('_')[-1])

            ekin = glob('*.ekin')[0]
            ekin = np.genfromtxt(ekin)
            pe = ekin[:, 4][-1]
            pes.append(pe)
            with tb.open_file("simulation.h5") as d:
                vx = d.root.simdata.vx[-1, 4, 4, rs/2:(rs/2)+rs]

            l = (len(vx) - rs)/2.
            vx = vx[l:l+rs]
            z = np.linspace(0, 1, len(vx))

            try:
                thflow = flow(z, pr, 0, 1, pmax)

                l2error = pa.l2_error(vx, exact=thflow)
                l2errorabs = pa.l2_error_abs(vx, exact=thflow)

                l2rel.append(l2error)
                l2abs.append(l2abs)
                res.append(rs)
            except:
                pass
            os.chdir(cp)

        #l2rel, l2abs, res = np.array(l2rel), np.array(l2abs), np.array(res)
        os.chdir(cdir)
        plt.plot(res, l2rel, mark, color = gen.next(), label = r'$\nu = {}$'.format(nu) , mew=0, ms=3, lw=0.5)

    os.chdir(plot_dir)
    plt.subplots_adjust(right=0.84, bottom=0.15)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),
                      ncol=1, fancybox=True, shadow=True, fontsize=7)
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Gridpoints N')
    plt.ylabel('$l_2$-rel. error')
    plt.xlim(7, 350)
    plt.ylim(5*1e-5, 2)
    #plt.show()
    plt.savefig('vp_convergence.pdf')

if __name__=='__main__':
    main()
