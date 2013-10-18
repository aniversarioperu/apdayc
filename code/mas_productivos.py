# -*- coding: utf-8 -*-
import codecs
import prettyplotlib as ppl
import numpy as np
from prettyplotlib import plt
import re

f = codecs.open("tmp_mas_productivos.txt", encoding="utf-8")
data = f.read()
f.close()

# This is the list of APDAYC directors "Comite Directivo"
apdayc = [
        "Escajadillo Farro",
        "Masse Fernandez",
        "Moreira Mercado",
        "Andrade Rios",
        "Cabrejos Bermejo",
        "Fuentes Barriga",
        "Montaño Jaramillo",
        "Rodriguez Grandez",
        "Laura Saavedra",
        "Bustamante Gomez"
        ]
x = []
y = []
bar_color = []
data = data.split("\n")
for i in data:
    if len(i) > 0:
        i = i.split(",")
        author = i[0].split(" ")
        author = author[0].capitalize() + " " + author[1].capitalize()

        if author in apdayc:
            bar_color.append("r")
        else:
            bar_color.append("#66c2a5")

        money = i[1].split(" ")
        total_money = money[len(money)-1]
        x.append(author)
        y.append(total_money)

y = map(float, y)

plt.rc('font', **{'family': 'DejaVu Sans'})
fig, ax = plt.subplots(1, figsize=(40,6))

width = 0.35
ind = np.arange(len(y))
xdata = ind + 0.05 + width
ax.bar(ind, y)
ax.set_xticks(ind + 0.5)
ax.set_xticklabels(x, rotation="vertical")
ax.autoscale()
ax.set_title(u'Los Asociados de APDAYC que cobraron más dinero en el 2012\nen color rojo figuran los miembros del Consejo Directivo',
        fontdict = {'fontsize':24}
        )

y_labels = ["0", "200,000", "400,000", "600,000", "800,000", "1,000,000"]
ax.set_yticklabels(y_labels)

plt.ylabel(u'Regalías en S/.', fontdict={'fontsize':18})
plt.xlabel(u'Beneficiario', fontdict={'fontsize':22})

print len(y)
print len(x)
ppl.bar(ax, np.arange(len(y)), y, grid="y", color=bar_color)
fig.tight_layout()
fig.savefig("output/mas_productivos.png")


###
# Que tal si ploteamos los socios principales, vitalicios y activos
f = codecs.open("data/socios_principales.tsv", encoding="utf-8")
data = f.read()
f.close()

bar_color = []
new_x = []
new_y = []

data = data.split("\n")

# keep all data in a dictionary
df = {}
for line in data:
    if len(line) > 0:
        line = re.sub("^\s+", "", line)
        line = re.sub("\s{2,}", "|", line)
        line = line.split("|")

        tmp = line[3].split(",")
        tmp2 = tmp[0].split(" ")
        try:
            author = tmp2[0].capitalize() + " " + tmp2[1].capitalize()
        except:
            continue

        if line[4] == "PRINCIPAL":
            index = x.index(author)

            money = y[index]
            df[money] = [author, "b"]

            x.remove(author)
            y.remove(y[index])

        elif line[4] == "VITALICIO":
            try:
                index = x.index(author)

                money = y[index]
                df[money] = [author, "g"]

                x.remove(author)
                y.remove(y[index])

            except:
                continue
        elif line[4] == "ACTIVO":
            try:
                index = x.index(author)

                money = y[index]
                df[money] = [author, "r"]

                x.remove(author)
                y.remove(y[index])

            except:
                continue
        else:
            try:
                index = x.index(author)

                money = y[index]
                df[money] = [author, "#D8D8D8"]

                x.remove(author)
                y.remove(y[index])

            except:
                continue

for author in x:
    index = x.index(author)
    money = y[index]
    df[money] = [author, "#D8D8D8"]

d = sorted(df, reverse=True)
for i in d:
    new_y.append(i)
    new_x.append(df[i][0])
    bar_color.append(df[i][1])


fig, ax = plt.subplots(1, figsize=(40,6))
ax.bar(ind, new_y)
ax.set_xticks(ind + 0.5)
ax.set_xticklabels(new_x, rotation="vertical")
ax.autoscale()
ax.set_title(u'Los Asociados de APDAYC que recibieron más regalías en el 2012',
        fontdict = {'fontsize':24}
        )

y_labels = ["0", "200,000", "400,000", "600,000", "800,000", "1,000,000"]
ax.set_yticklabels(y_labels)

plt.ylabel(u'Regalías en S/.', fontdict={'fontsize':18})
plt.xlabel(u'Beneficiarios', fontdict={'fontsize':22})
ppl.bar(ax, np.arange(len(new_y)), new_y, grid="y", color=bar_color)
fig.tight_layout()
fig.savefig("output/mas_productivos2.png")
