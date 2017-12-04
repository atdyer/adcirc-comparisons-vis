from math import sqrt

f14 = '/home/tristan/box/adcirc/runs/scaled20-refinement/original/fort.14'
fake = './data/fake.csv'
# center = [-78.009286, 33.883297]
center = [-77.977652, 33.946101]

# Read nodes
x = []
y = []
z = []
with open(f14, 'r') as f:

    f.readline()
    dat = f.readline().split()

    ne = int(dat[0])
    nn = int(dat[1])

    for i in range(nn):

        dat = f.readline().split()
        x.append(float(dat[1]))
        y.append(float(dat[2]))
        z.append(float(dat[3]))

xrange = [min(x), max(x)]
yrange = [min(y), max(y)]
def distance(xy):
    return sqrt((xy[0]-center[0])**2 + (xy[1]-center[1])**2)

dist = list(map(distance, zip(x, y)))
drange = [min(dist), max(dist)]

with open(fake, 'w') as f:

    f.write('x,y,error\n')

    bottom = 0
    top = 1
    cutoff = 0.172
    def smooth(v):
        return (v-cutoff) / (drange[1]-cutoff)

    for a, b, c, d in zip(x, y, z, dist):
        if c >= 0.0:
            d = drange[1] - d
            f.write('{},{},{}\n'.format(a, b, smooth(d) if d >= cutoff else 0))
        # f.write('{},{},{}\n'.format(a, b, c))