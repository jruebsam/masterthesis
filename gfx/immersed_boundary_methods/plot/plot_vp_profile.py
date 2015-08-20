import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import matplotlib.colors as colors
import matplotlib.cm as cmx


def tflow(x, pr, h1, h2, pmax):
    return -1/(2*pr)*pmax*(x**2 - x*(h1 + h2) + h1*h2)

def re2pr(re, pmax, h1, h2):
        return np.sqrt(-1/(2*re)*pmax*(h1*h2 - 0.25*(h1 + h2)**2))
#datafrom : /home/upgp/jruebsam/remake_sim/poiseuille_flow/o4_highres

def main():
    fpath = os.path.dirname(os.path.abspath(__file__))
    outpath = os.path.join(fpath, '..')

    with open('data/vp_o4hd/flows.pkl', 'rb') as f:
        flows =  pickle.load(f)

    f = plt.figure(figsize=(10, 5))
    ax = f.add_subplot(111)

    nus = []
    for nu, flow in flows.iteritems():
        nus.append(nu)
    nus = sorted(nus)

    jet = cm = plt.get_cmap('jet')
    cNorm  = colors.Normalize(vmin=0, vmax=len(nus))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
    values = range(len(nus))

    for idx, nu in enumerate(nus):
        flow = flows[nu]
        z = np.linspace(0, 2, len(flow))
        colorVal = scalarMap.to_rgba(values[idx])
        ax.plot(z, flow, color=colorVal, label=r'$\nu=%1.1e$' % nu)

    re=500.
    h1 = (32/127.)*2
    h2 = 2 - h1
    pr = re2pr(re, 10, h1, h2)
    flow=tflow(z, pr,h1,h2, 10)

    b = flow>-5
    ax.plot(z[b], flow[b], 'k--', label=r'theorie')

    ax.set_xlabel('Z')
    ax.set_ylabel('Geschwindigkeit v')

    ax.set_xlim(0, 2)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid()


    plt.savefig('/'.join([outpath, 'vp_flow.png']), dpi=300)
    #plt.show()



if __name__=='__main__':
    main()
