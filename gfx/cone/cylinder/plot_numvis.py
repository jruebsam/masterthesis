import style as style
style.setup()

import numpy as np
import matplotlib.pyplot as plt
import os, sys


cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']


#plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def nvis_o2(k, D, dx):
    return D/(dx**2)*(2*np.cos(k*dx) -2. )/(-D*k**2)

def nvis_o4(k, D, dx):
    return D/(12*dx**2)*(32*np.cos(k*dx) -2*np.cos(2*k*dx) - 30.)/(-D*k**2)

def main():
    f, ax = style.newfig(1., 0.5)

    dx = 1/128.
    ek = 1e-4
    l  = 1.

    breite = ek**(1./3.)
    lbr = 2*np.pi/(2*breite)

    plt.axvline(lbr, ls='--', color='red', linewidth=0.8,
            dashes = (1, 2, 5, 2), label=r'\delta\propto\text{Ek}^{1/3}')

    kmin = 2*np.pi/l
    kmax = 2*np.pi/(2*dx)

    k = np.linspace(kmin, kmax, 1001)

    ax.plot(k, nvis_o2(k, ek, dx), lw = 0.8, label = r'o2')
    ax.plot(k, nvis_o4(k, ek, dx), lw = 0.8,  label = r'o4')

    plt.legend(ncol = 1, fontsize=8, loc='upper right',
           fancybox=True, shadow=True)

    ax.set_ylim(0.3, 1.2)
    ax.set_xlim(0, 402)
    ax.set_xlabel(r'Wavevektor $K$')
    ax.set_ylabel(r'$D_{\mathrm{N}}/D_{\mathrm{P}}$')
    plt.subplots_adjust(bottom=0.2)

    ax.grid(True)
    plt.savefig('numvis.pdf')

if __name__=='__main__':
    main()
