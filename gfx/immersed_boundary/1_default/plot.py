import style
style.setup()

import numpy as np
import os
from scipy import optimize

import matplotlib.pyplot as plt

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def main():
    dpath = '/home/upgp/jruebsam/finaldata/noslip_validation/poiseuille_flow/1_default'

    labels = ['relative'] #absolute identisch zu absolut

    f, ax = style.newfig(0.8)

    o2_file = np.load(os.path.join(dpath, 'default_o2.npy'))
    res_o2, l2rel_o2, l2abs_o2 = o2_file.T

    o4_file = np.load(os.path.join(dpath, 'default_o4.npy'))
    res_o4, l2rel_o4, l2abs_o4 = o4_file.T


    fitfunc = lambda p, x: p[0]*x**p[1]
    errfunc = lambda p, x, y: fitfunc(p, x) - y
    p0 = [1., -2]
    p1, success = optimize.leastsq(errfunc, p0[:], args=(res_o4, l2rel_o4))

    xn = np.linspace(7, 160, 200)
    yn = fitfunc(p1, xn)

    ax.plot(xn, yn, label='fit: $ax^b$ : $b=%.3f$ +- ?' % p1[1])
    ax.plot(res_o2, l2rel_o2, '^--',  label='2nd-order')
    ax.plot(res_o4, l2rel_o4, 'h--', label='4th-order')

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.set_xlabel(r'gridpoints $N$')
    ax.set_ylabel(r'relative $l_2$-error')

    ax.set_xlim(5, 200)
    ax.set_ylim(1e-10, 1e-1)

    plt.legend()
    plt.grid()
    plt.tight_layout()
    #plt.show()
    plt.savefig('relative_l2error.pdf')

if __name__=='__main__':
    main()



