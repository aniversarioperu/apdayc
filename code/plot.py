# -*- coding: utf-8 -*-
import prettyplotlib as ppl
import numpy as np
from prettyplotlib import plt
import csv
from array import array


""" Top 20 ranking """
x = []
y = []
with open("tmp", "rb") as csvfile:
    f = csv.reader(csvfile, delimiter=",")
    for row in f:
        print row
        x.append(row[1])
        y.append(row[0])

# converts strings to int
y = map(int,y)

print x
print y

plt.rc('font', **{'family': 'DejaVu Sans'})
fig, ax = plt.subplots(1, figsize=(20,6))

width = 0.35
ind = np.arange(len(y))
xdata = ind + 0.05 + width
ax.bar(ind, y)
ax.set_xticks(ind + 0.5)
ax.set_xticklabels(x, rotation="vertical")
ax.autoscale()
ax.set_title(u'Ranking de canciones "Top 20"\n Radio Inspiración FM',
        fontdict = {'fontsize':24}
        )

plt.ylabel('Frecuencia en "Top 20"', fontdict={'fontsize':18})
plt.xlabel(u"Canción", fontdict={'fontsize':22})

ppl.bar(ax, np.arange(len(y)), y, grid="y")
fig.tight_layout()
fig.savefig("top20.png")
