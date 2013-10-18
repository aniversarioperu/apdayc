# -*- coding: utf-8 -*-
import prettyplotlib as ppl
import numpy as np
from prettyplotlib import plt
import csv
from array import array
import collections


""" Top 10 ranking """
x = []
y = []

ranks = ["1","2","3","4","5","6","7","8","9","10","maxima"]

with open("all_data.csv", "rb") as csvfile:
    f = csv.reader(csvfile, delimiter=",")
    for row in f:
        if row[0] in ranks:
            x.append(row[1])

counter = collections.Counter(x)
x = []
y = []
for i in sorted(counter, key=counter.get, reverse=True):
    if counter[i] != 1:
        x.append(i)
        y.append(counter[i])

for i in range(len(x)):
    print str(y[i]) + "," + str(x[i])


plt.rc('font', **{'family': 'DejaVu Sans'})
fig, ax = plt.subplots(1, figsize=(20,6))

width = 0.35
ind = np.arange(len(y))
xdata = ind + 0.05 + width
ax.bar(ind, y)
ax.set_xticks(ind + 0.5)
ax.set_xticklabels(x, rotation="vertical")
ax.autoscale()
ax.set_title(u'Ranking de canciones "Top 10"\n Radio Inspiración FM',
        fontdict = {'fontsize':24}
        )

plt.ylabel('Frecuencia en "Top 10"', fontdict={'fontsize':18})
plt.xlabel(u"Canción", fontdict={'fontsize':22})

ppl.bar(ax, np.arange(len(y)), y, grid="y")
fig.tight_layout()
fig.savefig("top10.png")

