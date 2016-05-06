import matplotlib.pyplot as plt
import numpy as np

from math import factorial as fac
from scipy import interpolate

import style
style.setup()

def radial_sort_line(x, y):
    """Sort unordered verts of an unclosed line by angle from their center."""
    # Radial sort
    x0, y0 = x.mean(), y.mean()
    angle = np.arctan2(y, x + 1.)

    idx = angle.argsort()
    x, y = x[idx], y[idx]

    # Split at opening in line
    dx = np.diff(np.append(x, x[-1]))
    dy = np.diff(np.append(y, y[-1]))
    max_gap = np.abs(np.hypot(dx, dy)).argmax() + 1

    x = np.append(x[max_gap:], x[:max_gap])
    y = np.append(y[max_gap:], y[:max_gap])
    return x, y

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']
from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def main():
    f, ax = style.newfig(0.8)

    x = np.linspace(-4, 4, 1500)
    X, Y = np.meshgrid(x, x)
    C = X + 1j*Y

    for i in range(1,6)[::-1]:

        b = np.zeros_like(C)
        for j in range(0,i):
            b += C**j/fac(j)

        out = np.where(np.diff((np.abs(b)<=1).astype('float')) != 0)
        pts = np.column_stack((X[out], Y[out]))

        x = pts[:, 0]
        y = pts[:, 1]

        try:
            x, y = radial_sort_line(x,y)
            x = np.append(x, x[0])
            y = np.append(y, y[0])

            tck, u = interpolate.splprep([x, y], s=0)
            unew = np.linspace(0, 1.0, 100)
            out = interpolate.splev(unew, tck)
            plt.plot(out[1], out[0], label='s = %i' % (i-1), lw=0.8)
        except:
            print i

    plt.axhline(0, ls='--')
    plt.axvline(0, ls='--')
    plt.grid()
    plt.legend()
    plt.subplots_adjust(top=0.8, bottom =0.15)
    ax.legend(ncol = 4,  loc='upper center', bbox_to_anchor=(0.5, 1.3),
           fancybox=True, shadow=True, title='RK-Method Order')

    plt.xlabel(r'$\Im(\lambda\Delta t)$')
    plt.ylabel(r'$\Re(\lambda\Delta t)$')
    plt.axes().set_aspect('equal')

    plt.savefig('rk_stability.pdf')



if __name__=='__main__':
    main()
