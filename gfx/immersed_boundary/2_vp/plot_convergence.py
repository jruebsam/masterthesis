import style
style.setup()

import numpy as np
import os
from scipy import optimize

import matplotlib.pyplot as plt

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def fd_o2(x, dx):
    return (x[2:]  - 2*x[1:-1] + x[:-2])/dx**2

def fd_o4(x, dx):
    return (-x[4:] +16*x[3:-1]  - 30*x[2:-2] + 16*x[1:-3]  -x[:-4])/(12*dx**2)

def main():
    dpath = '/home/upgp/jruebsam/finaldata/noslip_validation/poiseuille_flow/2_vp/'

    o2_prof = np.load(os.path.join(dpath, 'profile_o2.npy'))
    o4_prof = np.load(os.path.join(dpath, 'profile_o4.npy'))
    th_prof = np.load(os.path.join(dpath, 'profile_th.npy'))

    f = plt.figure(figsize=style.figsize(0.8))
    ax = f.add_subplot(121)
    ax2 = f.add_subplot(222)
    ax3 = f.add_subplot(224)
    ##AX3
    z, vx = o2_prof.T
    N = 64
    dx = 1/(N-1.)
    zl = np.linspace(-1, 0, 64)
    zr = np.linspace(1, 2, 64)

    nl = np.zeros(N-1)

    #zn = np.hstack((zl[:-1], z, zr[1:]))
    #vn = np.hstack((nl, vx, nl))

    zn, vn = z, vx

    ax3.plot(zn[1:-1], fd_o2(vn, dx), 'bo--')
    ax3.plot(zn[2:-2], fd_o4(vn, dx), 'go--')
    #ax3.plot(zn, vn, 'bo--')

    ax3.set_xlim(-0.1, 0.2)
    ax3.set_ylim(-1, 10)

    ##AX2
    ps = [o2_prof, o4_prof, th_prof]
    label = ['o2', 'o4', 'th']
    mss = ['o--', '^--', '--']

    for profile, m in zip(ps, mss):
        z, vx = profile.T

        ax2.plot(z, vx, m, ms=4, mew=0, lw=1)

    ax2.set_xlabel(r'z')
    ax2.set_ylabel(r'Velocity $v_x$')
    ax2.set_xlim(-0.1, 0.2)
    ax2.set_ylim(-1, 10)

    plt.grid()
    plt.tight_layout()
    plt.show()
    #style.savefig('vp_convergence')

if __name__=='__main__':
    main()



