import style
style.setup()

import numpy as np
import pycurb.analysis as pa
import tables as tb
import os
from scipy import optimize

import matplotlib.pyplot as plt

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']

from cycler import cycler
plt.rc('axes', prop_cycle=(cycler('color', cmap)))

def theo(x, a=1, o=0):
    h1 = 0.5
    h2 = 1.5
    return -4*a*(x**2 - x*(h1 + h2) + h1*h2) + o

def profile(a=10, o=0.1, A=0.5):
    xl = np.linspace(0, 0.5, 101)
    yl = np.exp((xl-0.5)*a)*o
    xm = np.linspace(0.5, 1.5, 201)
    ym = theo(xm, A, o)
    xr = np.linspace(1.5, 2., 101)
    yr = yl[::-1]
    x = np.append(xl, xm)
    x = np.append(x, xr)
    y = np.append(yl, ym)
    y = np.append(y, yr)
    return x,y

def main():
    f, ax = style.newfig(0.45, 1.5)

    ax.set_xlabel(r'Height z')
    ax.set_ylabel(r'Velocity $v_x$')

    ds = (1, 2, 5, 2)

    x, y = profile(a=13, A = 0.7)
    plt.plot(x,y, '--', ms=0.8, label=r'$N<N_{min}$', dashes=ds)

    x, y = profile(a=10, o= 0.3, A=0.9)
    plt.plot(x,y, ms=0.8, label=r'Theor. Exact')

    x, y = profile(a=15, o= 0.15, A=0.8)
    plt.plot(x,y, '--', ms=0.8, label=r'$N=N_{min}$', dashes=ds)

    xt = np.linspace(0.5, 1.5, 201)
    plt.plot(xt, theo(xt), ms=0.8,label=r'Theor. Assumed')

    x, y = profile(a=10, o= 0.25, A=0.85)
    plt.plot(x,y, '--', ms=0.8, label=r'$N>N_{min}$', dashes=ds)



    ax.legend(ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1.4),
           fancybox=True, shadow=True, fontsize=7)
    plt.subplots_adjust(top=0.75, bottom=0.15, left=0.15)


    plt.grid()
    #plt.show()
    plt.savefig('profile.pdf')

if __name__=='__main__':
    main()



