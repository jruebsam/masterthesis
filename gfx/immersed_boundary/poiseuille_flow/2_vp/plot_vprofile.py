import style
style.setup()

from glob import glob
import numpy as np
import tables as tb
import matplotlib.pyplot as plt
import os
import matplotlib.colors as colors
import matplotlib.cm as cmx

def tflow(x, pr, h1, h2, pmax):
    return -1/(2*pr)*pmax*(x**2 - x*(h1 + h2) + h1*h2)

def re2pr(re, pmax, h1, h2):
        return np.sqrt(-1/(2*re)*pmax*(h1*h2 - 0.25*(h1 + h2)**2))

def main():
    plot_path = os.getcwd()

    dpath = '/home/upgp/jruebsam/simulations/feb16/week2/2_vp_error_nu_re/'
    os.chdir(dpath)

    paths = sorted(glob('data/*/*o2*'), key=lambda x: float((x.split('/')[1]).split('_')[-1]))

    nus, profiles = [], []
    rs = 128

    cdir = os.getcwd()
    for path in paths:
        print "Reading path %s " % path
        os.chdir(path)

        sim_paths = sorted(os.listdir(os.getcwd()), key=lambda x: int(x.split('_')[-1]))
        nus.append(float(((path.split('/')[1]).split('_')[-1])))

        for sp in sim_paths:
            re = float(sp.split('_')[-1])
            if re==100:

                with tb.open_file(os.path.join(sp, "simulation.h5")) as d:
                    vx = d.root.simdata.vx[-1, 4, 4]

                profiles.append(vx)
        os.chdir(cdir)
    os.chdir(plot_path)

    f, ax = style.newfig(0.8)

    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=len(nus))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    values = range(len(nus))

    for idx, nu in enumerate(nus):
        flow = profiles[idx]
        z = np.linspace(0, 2, len(flow))
        colorVal = scalarMap.to_rgba(values[idx])
        ax.plot(z, flow, color=colorVal, label=r'$\nu={}$'.format(nu))


    z = np.linspace(0, 2, rs)
    re=100.
    h1 = (32/127.)*2
    h2 = 2 - h1
    pr = re2pr(re, 10, h1, h2)
    flow=tflow(z, pr,h1,h2, 10)
    b = flow>-5
    ax.plot(z[b], flow[b], 'k--', label=r'theorie')

    ax.set_xlabel('Z')
    ax.set_ylabel('Geschwindigkeit v')

    ax.set_xlim(0, 2)
    ax.set_ylim(-3, 22)

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid()

    plt.subplots_adjust(right=0.8, bottom=0.15)
    plt.savefig('vp_profile.pdf')
    #plt.show()



if __name__=='__main__':
    main()
