import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colorbar as colbar
from matplotlib.colors import LinearSegmentedColormap

def get_xyz_fromcsv(csv_file_path):

    data = np.genfromtxt(csv_file_path, delimiter=',', dtype=float, skip_header=1)
    data = data[~np.isnan(data).any(axis=1)]

    # Return all the data
    return data

def gen_map(data):

    cmap = ['#0000ff', '#00ffff', '#ffffff', '#00ff00', '#00af00', '#006400']
    # cmap = ['#006400', '#00af00', '#00ff00', '#ffffff', '#00ffff', '#0000ff']

    cmap = LinearSegmentedColormap.from_list('mesh', cmap)

    x = data[:,0]
    y = data[:,1]
    z = data[:,2]

    drange = [np.min(z), np.max(z)]
    def fmt(_x, _pos):
        val = drange[0] + _x * (drange[1]-drange[0])
        return '{:.2f}'.format(val)

    fig = plt.figure()
    ax1 = fig.add_axes([0.05, 0.1, 0.8, 0.8])
    ax2 = fig.add_axes([0.87, 0.1, 0.05, 0.8])

    ax1.scatter(x, y, c=z, cmap=cmap, s=3.5)
    ax1.set_aspect('equal')

    colbar.ColorbarBase(
        ax2,
        cmap=cmap,
        orientation='vertical',
        label='Nodal Elevation (m)',
        format=ticker.FuncFormatter(fmt)
    )

    plt.show()

if __name__ == '__main__':

    if len(sys.argv) == 2:

        d = get_xyz_fromcsv(sys.argv[1])
        gen_map(d)