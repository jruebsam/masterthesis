import numpy as np
import os
import matplotlib.pyplot as plt

def main():
    name = 'mask.png'
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', name)
    f = plt.figure()
    ax = f.add_subplot(111)


    p = np.linspace(0, 1, 64)
    x, y = np.meshgrid(p,p)

    H = 1-((x-0.5)**2+(y-0.5)**2 < 0.8*0.5**2).astype('int')

    ax.imshow(H, interpolation='nearest',extent =[0, 1, 0,1 ])
    ax.scatter(x.flatten(), y.flatten(), s=4., c='y', alpha=0.7)


    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    plt.savefig(path, dpi=200)



if __name__=='__main__':
    main()
