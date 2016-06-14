import style
style.setup()
import numpy as np
import tables as tb
import matplotlib.pyplot as plt

from scipy.special import jn, jvp
from scipy.optimize import brentq

from scipy.optimize import fsolve
from scipy.signal import argrelmin

import pycurb.analysis as pa
from custommap import bipolar


def f(e):
    J = jn(1, e)
    return e*J

def main():
    p1 = '/home/upgp/jruebsam/simulations/april16/week2/cylinder_series/data/df/o2/omg_1.2/'
    p2 = '/home/upgp/jruebsam/simulations/april16/week2/cylinder_series/data/df/o2/omg_0.7/'
    p3 = '/home/upgp/jruebsam/simulations/april16/week2/cylinder_series/data/df/o2/omg_1.7/'
    ps = [p1, p2, p3]

    ns =  [ 2, 2, 4]
    ms =  [ 1, 2, 1]
    c = bipolar(neutral=0, lutsize=1024)

    x = np.linspace(0, 40,200000)
    y = f(x)*f(x)
    roots = argrelmin(y)[0]

    fig, axes = plt.subplots(2, 3, figsize=style.figsize(0.9))
    print axes.shape

    for ax, text in zip([axes[0, 2], axes[1, 2]], ['Theory', 'Simulation']):
        # build a rectangle in axes coords
        left, width = .25, .5
        bottom, height = .25, .5
        right = left + width
        top = bottom + height
        of = 0.3
        ax.text(right + 0.4, 0.5*(bottom+top), text,
                fontsize=12,
                horizontalalignment='left',
                verticalalignment='center',
                rotation='vertical',
                transform=ax.transAxes)


    axes[0, 0].set_ylabel(r'$\nabla p\cdot \vec{e}_z$')
    axes[1, 0].set_ylabel(r'$\int \mathrm{dt}|v_z(y=1/2)|$')
    for ax, n, m in zip(axes[0], ns, ms):
        r = 0.5
        H = 1.1
        X, Z = np.mgrid[-r:r:101*1j, 0:1:101*1j]
        a = r/H
        r = X
        eps = x[roots[m-1]]

        l = 2/np.sqrt((1 + eps**2/((n*np.pi*a)**2)))

        phi = jn(0, eps*r/a)*np.cos(n*np.pi*Z)
        gx, gz = np.gradient(phi)
        phi = gz#np.sqrt(gx**2 + gz**2)
        ax.imshow(phi.T, origin='lower', extent=[0, 1, 0, 1.1] )
        ax.set_title(r'$(n,m)=(%i,%i)$' % (n, m))

    for ax, p in zip(axes[1], ps):
        d = pa.DataTool(p)
        d.grab_plane( ['xz'],['vz'])

        v = np.sum(np.abs(d.planes.xz.vz[800:]), axis=0)

        ax.imshow(v.T, origin='lower', extent=[-0.05, 1.05, 0, 1.1] )
        ax.set_xlim(0, 1)


    plt.savefig('modes.pdf')

if __name__=='__main__':
    main()
