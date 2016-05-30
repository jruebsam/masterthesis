import style
style.setup()
import numpy as np
import tables as tb
import matplotlib.pyplot as plt

plt.rcParams['text.latex.preamble']=r'\makeatletter \newcommand*{\rom}[1]{\expandafter\@slowromancap\romannumeral #1@} \makeatother'
plt.rcParams.update()

import sys, os

from custommap import bipolar

def main():
    pfrustum = '/home/upgp/jruebsam/simulations/mai16/week5/series_offset_l2/data'
    pcone = '/home/upgp/jruebsam/simulations/mai16/week5/series_offset_with_tip_l2/data'

    p1 = {'omg': 1.25, 'path':pfrustum, 'label'   : r'M\rom{1} Frustum',
          'frame':50, 'offset':25, 'h': 0.25}

    p2 = {'omg': 1.25, 'path':pcone   , 'label'   : r'M\rom{1} Cone',
          'frame':70, 'offset':15, 'h': 0.25}

    p3 = {'omg': 0.9,  'path':pfrustum  , 'label' : r'M\rom{2} Frustum',
          'frame':60, 'offset':30, 'h': 0.25}

    p4 = {'omg': 0.85, 'path':pcone   , 'label'   : r'M\rom{8} Cone',
          'frame':50, 'offset':30, 'h': 0.25}

    fig, axes = plt.subplots(2, 4, figsize=style.figsize(1.0))
    c = bipolar(neutral=0, lutsize=1024)

    for ax, p in zip(axes.T, [p1, p2, p3, p4]):
        h, omg, pt   =  p['h'], p['omg'], p['path']
        label = p['label']
        frame1 = '%08i.h5' % p['frame']
        frame2 = '%08i.h5' % (p['frame'] + p['offset'])

        dp1 = os.path.join(pt, 'h_%.3f' % h, 'omg_%.2f' % omg, 'gfx', frame1)
        dp2 = os.path.join(pt, 'h_%.3f' % h, 'omg_%.2f' % omg, 'gfx', frame2)

        if 'Frustum' in label:
            e = [0, 1, 0.375, 1.25]
        else:
            e = [0, 1, 0 , 1.25]

        with tb.open_file(dp1, 'r') as d:
            vz = d.root.xz.vz[:]
        lim = np.max(np.abs(vz))
        cm1 = ax[0].imshow(vz.T, origin='lower', cmap = c, extent=e, vmin=-lim, vmax=lim)

        with tb.open_file(dp2, 'r') as d:
            vz = d.root.xz.vz[:]
        lim = np.max(np.abs(vz))
        cm1 = ax[1].imshow(vz.T, origin='lower', cmap = c, extent=e, vmin=-lim, vmax=lim)

        ax[0].set_title(label)

        for a in ax:
            a.set_ylim(0, 1.25)
            a.set_axis_bgcolor('black')
            a.xaxis.set_major_locator(plt.NullLocator())
            a.yaxis.set_major_locator(plt.NullLocator())

    plt.subplots_adjust(bottom=0.2, top =0.9, hspace=0.05, wspace=0.05)

    cbar_ax = fig.add_axes([0.15, 0.1, 0.72, 0.03])
    cb = fig.colorbar(cm1, cax=cbar_ax, orientation='horizontal')
    cb.set_ticks([])
    cb.set_label(r'$\propto v_z$')

    axes[0, 0].set_ylabel(r'$t_0$')
    axes[1, 0].set_ylabel(r'$t_0 + \Delta t^*$')
    plt.savefig('modes.pdf')

if __name__=='__main__':
    main()
