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

    f = plt.figure(figsize=style.figsize(0.4))
    ax = f.add_subplot(111)
    n, l2rel, l2abs = np.load(os.path.join(dpath, 'o2_out.npy')).T
    ax.plot(n, l2rel,'o--',  label='o2')
    n, l2rel, l2abs = np.load(os.path.join(dpath, 'o4_out.npy')).T
    ax.plot(n, l2rel,'o--',  label='o4')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('TODO->')
    ax.set_ylabel('$l_2$-relative error')

    """
    o2_prof = np.load(os.path.join(dpath, 'profile_o2.npy'))
    o4_prof = np.load(os.path.join(dpath, 'profile_o4.npy'))
    th_prof = np.load(os.path.join(dpath, 'profile_th.npy'))


    ax1 = f.add_subplot(222)
    ax2 = f.add_subplot(224)

    #AX1
    z, vx = o2_prof.T
    z2, vx2 = o4_prof.T
    N = 64
    dx = 1/(N-1.)

    ax1.plot(z, vx, 'go--')
    ax1.plot(z2, vx2, 'yo--')
    ax1.set_xlim(0-dx*2, 0+dx*2)
    ax1.set_ylim(-1, 1)

    ##AX2
    ps = [o2_prof, o4_prof, th_prof]
    label = ['o2', 'o4', 'th']
    mss = ['o--', '^--', '--']

    for profile, m in zip(ps, mss):
        z, vx = profile.T

        ax2.plot(z, vx, m, ms=4, mew=0, lw=4)

    ax2.set_xlabel(r'z')
    ax2.set_ylabel(r'Velocity $v_x$')
    ax2.set_xlim(-0.1, 0.2)
    ax2.set_ylim(-1, 10)
    """

    plt.grid()
    #plt.tight_layout()
    #plt.show()
    plt.savefig('vp_convergence.pdf')

if __name__=='__main__':
    main()



