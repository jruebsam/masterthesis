import style
style.setup()

from scipy.signal import argrelmin, argrelmax
from matplotlib.patches import Polygon
import numpy as np
import matplotlib.pyplot as plt
import os, sys
from matplotlib import ticker
from glob import glob
import tables as tb
import pycurb.analysis as pa
from scipy import stats
import itertools as it
import itertools
from scipy import optimize

from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

cmap = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf']
markers = itertools.cycle('o^*')
from cycler import cycler

cc = itertools.cycle(plt.cm.spectral(np.linspace(0,1,10)))
#plt.rc('axes', prop_cycle=(cycler('color', cmap)))
plt.rcParams['text.latex.preamble']=r'\makeatletter \newcommand*{\rom}[1]{\expandafter\@slowromancap\romannumeral #1@} \makeatother'
plt.rcParams.update()

def get_omg(w, r):
    gamma = np.arccos(w/2.)
    hc = 0.5*np.tan(np.pi/3.)
    hr = np.tan(gamma)*0.5
    d = (hc - hr)*(0.5 - r)/hc
    beta = np.arctan(hr/(0.5 - d))
    return 2*np.cos(beta)


def get_amp_old(series):
    n = len(series)/4
    data = series[3*n:]
    A = 0.5*(np.max(data)-np.min(data))
    return A

def get_amp(x):
    maxids = argrelmax(x)[0][-2:]
    minids = argrelmin(x)[0][-2:]

    ids = np.sort(np.append(maxids, minids))

    amp = 0.5*(np.abs(x[ids[3]] - x[ids[2]]))
    old = 0.5*(np.abs(x[ids[1]] - x[ids[0]]))

    rel_error = np.abs(amp-old)/amp
    return amp, rel_error

def main():
    dpath1 = '/home/upgp/jruebsam/simulations/mai16/week5/series_offset_l2/'
    dpath2 = '/home/upgp/jruebsam/simulations/mai16/week5/series_offset_with_tip_l2/'

    rs = np.linspace(0, 0.5, 5)[::-1]
    cdir = os.getcwd()

    f, axes = plt.subplots(len(rs), 2, figsize=style.figsize(1., np.sqrt(2)),
                            gridspec_kw = {'width_ratios':[3, 1]})
    # build a rectangle in axes coords
    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width + 0.5
    top = bottom + height

    l =  0.5*np.tan(np.pi/3.)
    for ax, radius in zip(axes[:, 1], rs):
        h = radius
        r = 0.21650635094610973
        hc = 0.5*np.tan(np.pi/3.)

        p00 = (0.5-r, 0.375)
        p01 = (0.5+r, 0.375)
        p11 = (1,hc )
        p10 = (0, hc )
        po2= (1, 1 + h )
        po = (0, 1 + h )
        cube_lines = [p00, p01, p11, po2, po, p10]
        x = [p[0] for p in cube_lines]
        y = [p[1] for p in cube_lines]
        d = np.column_stack((x,y))
        p = Polygon(d, alpha=0.5, color='b', hatch='x')
        ax.add_artist(p)

        p00 = (0.5, 0)
        p01 = (0.5 +r, 0.375)
        p11 = (0.5 -r, 0.375)
        cube_lines = [p00, p01, p11]
        x = [p[0] for p in cube_lines]
        y = [p[1] for p in cube_lines]
        d = np.column_stack((x,y))
        p = Polygon(d, alpha=0.5, color='g', hatch='x')
        ax.add_artist(p)

        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xlabel('x', labelpad = 0.1)
        ax.set_ylabel('z', labelpad = 0.1)
        ax.xaxis.labelpad = -5
        ax.set_aspect('equal')
        ax.set_ylim(0, 1.5)
        ax.text(right, 0.5*(bottom+top), r'$h_+=%.3f$' % h,
                horizontalalignment='center',
                verticalalignment='center',
                rotation='vertical',
                transform=ax.transAxes)

    hs = rs
    for i, (ax, radius) in enumerate(zip(axes[:, 0], hs)):

        for label, dpath in zip(['Frustum', 'Cone'], [dpath1, dpath2]):
            os.chdir(os.path.join(dpath, 'data', 'h_%.3f' % radius))

            simpathes =  glob('*/*.ekin')

            omgs = sorted([float((x.split('/')[0]).split('_')[-1]) for x in simpathes])

            a_ekin, a_vz, a_vphi = [], [], []
            omgsn = []

            for j, simpath in enumerate(sorted(simpathes)):
                #print simpath
                data = np.genfromtxt(simpath)
                time = data[:, 0]
                ekin = data[:, 1]
                vz   = data[:, -3]
                vphi = data[:, -1]
                #ax.plot(time, vz, label=simpath)
                #a_ekin.append(get_amp(ekin))

                amp, _ = get_amp(vz)
                #a_vphi.append(get_amp(vphi))

                #plt.plot(time, vz, label=simpath.split('/')[-1])
                a_vz.append(amp)
                omgsn.append(omgs[j])

            if i>0:
                ax.plot(omgsn, a_vz, 'o-',  ms=3, mew=0, alpha=0.8)
            else:
                ax.plot(omgsn, a_vz, 'o-',  ms=3, mew=0, alpha=0.8, label=label)

        if i>0:
            ax.axvline(1, color='#e41a1c', lw=0.75)
        else:
            ax.axvline(1, color='#e41a1c', lw=0.75, label=r'Crit.Slope $\alpha = \theta$')
        ax.set_ylabel(radius)
        os.chdir(cdir)

        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-2,-3))
        ax.yaxis.set_major_formatter(formatter)

        ax.set_ylabel(r'$A\left(\left<v_z^2\right>\right)$')
        ax.grid(True)
        ax.set_ylim(0, 5*1e-4)
        ax.set_xlim(0.2, 2)


    for i, ax in enumerate(axes[:, 1]):
        if i == 0:
            ax.set_title('Setup')

    #ap=dict(facecolor='black', width=0.3, headwidth=3., headlength =3)
    ap=dict(arrowstyle='-|>' , facecolor='black', lw=0.8
            )
    kw=dict(size=10., horizontalalignment='center', verticalalignment='bottom')

    for i, ax in enumerate(axes[:, 0]):
        if i == 0:
            ax.annotate(r'(\rom{6})', xy=(1.8, 0.0001),
                        xytext=(1.8, 0.0002), arrowprops=ap, **kw)

            ax.annotate(r'(\rom{7})', xy=(0.55, 0.0002),
                        xytext=(0.55, 0.00035),  arrowprops=ap, **kw)

            ax.annotate(r'(\textbf{O})', xy=(1.1, 0.00015),
                        xytext=(1.1, 0.00005), arrowprops=ap, **kw)
        if i == 2:
            ax.annotate(r'(\rom{1})', xy=(1.25, 0.0004),
                        xytext=(1.25, 0.0002), arrowprops=ap, **kw)

            ax.annotate(r'(\rom{2})', xy=(0.85, 0.00038),
                        xytext=(0.7, 0.0004),  arrowprops=ap, **kw)

            ax.annotate(r'(\rom{3})', xy=(0.5, 0.00025),
                        xytext=(0.5, 0.0001),  arrowprops=ap, **kw)

            ax.annotate(r'(\rom{5})', xy=(1.5, 0.0001),
                        xytext=(1.5, 0.0002),  arrowprops=ap, **kw)

            ax.annotate(r'(\rom{4})', xy=(1.7, 0.0001),
                        xytext=(1.7, 0.0002),  arrowprops=ap, **kw)

            ax.annotate(r'(\rom{8})', xy=(0.85, 0.00029),
                        xytext=(0.85, 0.0001),  arrowprops=ap, **kw)
        if i < 4:
            labels = [item.get_text() for item in ax.get_xticklabels()]
            empty_string_labels = ['']*len(labels)
            ax.set_xticklabels(empty_string_labels)
        else:
            ax.set_xlabel(r'$\omega$')

    plt.sca(axes[0, 0])
    plt.legend(ncol = 3, fontsize=9, loc='upper center', bbox_to_anchor=(0.5, 1.4),
           fancybox=True, shadow=True)

    plt.subplots_adjust(bottom =0.05, top =0.9)

    plt.savefig('transition.pdf')

if __name__=='__main__':
    main()
