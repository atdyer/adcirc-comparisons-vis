import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interp
import matplotlib.colors as col
import matplotlib.colorbar as colbar
import matplotlib.ticker as ticker


def get_xyz_fromcsv(csv_file_path):

    data = np.genfromtxt(csv_file_path, delimiter=',', dtype=float, skip_header=1)
    data = data[~np.isnan(data).any(axis=1)]

    # Return all the data
    return data
    
def plot_range(axis, data, minval, maxval, color, size):

    d = data[np.logical_and(data[:,2] >= minval, data[:,2] < maxval)]
    axis.plot(d[:,0], d[:,1], '.', c=color, ms=size)

def gen_map(data, cm='pink'):

    fig = plt.figure()
    ax1 = fig.add_axes([0.05, 0.1, 0.8, 0.8])
    ax2 = fig.add_axes([0.87, 0.1, 0.05, 0.8])

    # Choose the colors
    cmaps = {
        'pink': ['#f7f4f9','#e7e1ef','#d4b9da','#c994c7','#df65b0','#e7298a','#ce1256','#980043','#67001f'],
        'blue': ['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494','#081d58'],
        'green': ['#f7fcf0','#e0f3db','#ccebc5','#a8ddb5','#7bccc4','#4eb3d3','#2b8cbe','#0868ac','#084081'],
        'gray': ['#ffffff','#f0f0f0','#d9d9d9','#bdbdbd','#969696','#737373','#525252','#252525','#000000']
    }

    colors = cmaps[cm] if cm in cmaps else cmaps['pink']
    # colors = list(reversed(colors))

    # Create ranges
    minz = np.min(data[:,2])
    maxz = np.max(data[:,2])
    bins = [minz + i*((maxz-minz)/(len(colors))) for i in range(len(colors)+1)]

    # Print some output
    print('Data range: [', minz, ',', maxz, ']')

    # Plot the data
    for i in range(len(colors)):
        color = colors[i]
        if i == 0:
            size = 3.5
            plot_range(ax1, data, bins[i], bins[i]+0.01, '#000000', size)
        else:
            size = 3.5
            low = bins[i]
            high = bins[i+1]
            plot_range(ax1, data, low, high, color, size)

    # Set axis aspect
    ax1.set_aspect('equal')

    # Make the colorbar
    def fmt(_x, _pos):
        return '{:.2f}'.format(_x)
    cmap = col.ListedColormap(colors)
    norm = col.BoundaryNorm(bins, cmap.N)
    colbar.ColorbarBase(
        ax2,
        cmap=cmap,
        norm=norm,
        orientation='vertical',
        label='Error (m)',
        format=ticker.FuncFormatter(fmt)
    )

    # Show the lot
    plt.show()


if __name__ == "__main__":

    cmap = 'pink'

    if len(sys.argv) == 2:

        data = get_xyz_fromcsv(sys.argv[1])

    elif len(sys.argv) == 3:

        data = get_xyz_fromcsv(sys.argv[1])
        cmap = sys.argv[2]

    else:

        print('python adcircvisualize.py [csv file]')
        print('python adcircvisualize.py [csv file] [colormap]')
        print('\t\t[colormap] must be one of pink, blue, green, or gray')
        exit()

    gen_map(data, cm=cmap)