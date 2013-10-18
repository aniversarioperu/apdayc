# -*- coding: utf-8 -*-
import codecs
import locale
import prettyplotlib as ppl
import numpy as np
from prettyplotlib import plt

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


f = codecs.open("output/tmp_socios_principales.txt", encoding="utf-8")
data = f.read()
f.close()

# Esta es la lista de "Socios principales"
data = data.split("\n")
principales = []
vitalicios = []
activos = []
for line in data:
    line = line.strip()
    if len(line) > 0:
        line = line.split(",")
        if line[1] == "PRINCIPAL":
            principales.append(line[0])
        if line[1] == "VITALICIO":
            vitalicios.append(line[0])
        if line[1] == "ACTIVO": 
            activos.append(line[0])

# cantidad de regalias por "socios principales"
f = codecs.open("output/tmp_mas_productivos.txt", encoding="utf-8")
data = f.read()
f.close()

data = data.split("\n")
princi_money = float()
vitali_money = float()
activo_money = float()
otros_money = float()

for i in data:
    if len(i) > 0:
        i = i.split(",")
        author = i[0]
        money = i[1].split(" ")
        money = money[len(money)-1]
        if author in principales:
            princi_money += float(money)
        elif author in vitalicios:
            vitali_money += float(money)
        elif author in activos:
            activo_money += float(money)
        else:
            otros_money += float(money)

## DO principales + vitalicios
## numero de socios por categoria
numero_socios = [str(len(principales) + len(vitalicios)),
                 str(250-len(principales)-len(vitalicios))]

print "Socios privilegiados con el voto " + str(len(principales) +
        len(vitalicios) + len(activos))

y = [princi_money + vitali_money, activo_money + otros_money]
annotate = [locale.format("%d", y[0], grouping=True) + " S/.",
            locale.format("%d", y[1], grouping=True) + " S/."]

width = 0.35
bar_color = ["r", "#66c2a5"]
plt.rc('font', **{'family': 'DejaVu Sans'})
fig, ax = plt.subplots(1, figsize=(8,6))
ind = np.arange(2)
xdata = ind + 0.05 + width
ax.bar(ind, y)
ax.set_xticks(ind + 0.4)
ax.set_xticklabels(["principales y vitalicios\n(" + numero_socios[0] + " socios)", 
                    "otros socios\n(" + numero_socios[1] + " socios)", 
                    ],
                    rotation="horizontal", multialignment="center")
ax.autoscale()
ax.set_title(u'Ganancias de socios principales y vitalicios\n comparados con el resto de socios',
        fontdict = {'fontsize':22}
        )

y_labels = ["0", "1,000,000", "2,000,000", "3,000,000", "4,000,000",
                "5,000,000", "6,000,000", "7,000,000", "8,000,000"]
ax.set_yticklabels(y_labels)

plt.ylabel(u'Regalías en S/.', fontdict={'fontsize':18})
plt.xlabel(u'Beneficiarios', fontdict={'fontsize':22})

ppl.bar(ax, np.arange(len(y)), y, grid="y", annotate=annotate, color=bar_color)
fig.tight_layout()
fig.savefig("output/socios_principales.png")
output = "Plot de socios Principales + Vitalicios guardados en archivo "
output += "``output/socios_principales.png``\n"
print output


## DO principales + vitalicios + activos
## numero de socios por categoria
numero_socios = [str(len(principales) + len(vitalicios) + len(activos)),
                 str(250-len(principales) - len(vitalicios) - len(activos))]

# Porcentaje de socios principales+vitalicios+activos versus otros
percent_pva = float((len(principales)+len(vitalicios)+len(activos))*100/250)
percent_socios_otros = 100.0 - percent_pva

# Porcentaje de DINERO de socios principales+vitalicios+activos versus otros
y = [princi_money + vitali_money + activo_money, otros_money]
percent_money_pva = int(float(princi_money + vitali_money + activo_money)*100/(y[0] + y[1]))
percent_money_otros = 100 - percent_money_pva

annotate = [locale.format("%d", y[0], grouping=True) +
                " S/.",
            locale.format("%d", y[1], grouping=True) + 
                " S/."]

width = 0.35
bar_color = ["r", "#0099FF"]
plt.rc('font', **{'family': 'DejaVu Sans'})
fig, ax = plt.subplots(1, figsize=(9,6))
ind = np.arange(2)
xdata = ind + 0.05 + width

# write percentaje of money to plot
ax.annotate(str(percent_money_pva) +"%\ndel dinero", ha="center", color="w",
        size=38, xy=(0.2,1.2), xytext=(0.4, 2500000))
ax.annotate(str(percent_money_otros) +"%\ndel dinero", ha="center", color="w",
        size=18, xy=(0.2,1.2), xytext=(1.4, 150000))

ax.bar(ind, y)
ax.set_xticks(ind + 0.4)
ax.set_xticklabels(["principales, vitalicios y activos\n(" +
                            str(int(percent_pva)) + "% del total)", 
                    "otros socios\n(" + 
                            str(int(percent_socios_otros)) + "% del total)"
                    ],
                    rotation="horizontal", multialignment="center")
ax.autoscale()
ax.set_title(u'Ganancias de socios principales, vitalicios y activos' 
        + '\ncomparados con el resto de socios',
        fontdict = {'fontsize':22}
        )

y_labels = ["0", "1,000,000", "2,000,000", "3,000,000", "4,000,000",
                "5,000,000", "6,000,000", "7,000,000", "8,000,000"]
ax.set_yticklabels(y_labels)

plt.ylabel(u'Regalías en S/.', fontdict={'fontsize':18})
plt.xlabel(u'Beneficiarios', fontdict={'fontsize':22})

ppl.bar(ax, np.arange(len(y)), y, annotate=annotate, color=bar_color)
fig.tight_layout()
fig.savefig("output/socios_principales_vitalicios_activos.png")
output = "Plot de socios Principales + Vitalicios + Activos guardados en archivo "
output += "``output/socios_principales_vitalicios_activos.png``\n"
print output



# Que tal si vemos qué porcentaje de socios se lleva qué porcentaje de TODO el
# dinero repartido, no solo lo repartido a los 250 socios "más productivos"
# 
# En la Memoria de APDAYC del 2012, señalan en la pagina 12 (o página 22 en
# realidad, que en ese año se repartieron 29 millones de soles entre todos sus
# asociados.
#
# Según el útero de marita ( http://bit.ly/18HEiF5 )
# "APDAYC tiene más de 8 mil afiliados, pero sólo 248 tienen derecho a voto en
# la Asamblea General"
# 
# Digamos que son 8 mil exactos, entonces entre ellos repartió 29 millones
# durante el 2012. 
# 
# * Qué porcentaje de estos 8mil son los socios con votos privilegiados
#   (principales, vitalicios y activos).
# * Qué porcentaje del dinero total se llevan estos socios con voto
#   privilegiado?

# Memoria 2012, pagina 22, regalías distribuidas en el 2012:
# 29,197,272 soles
total_money = 29197272.0
total_socios = 8000.0

# Tenemos socios principales + vitalicios + activos
print "Total socios con voto privilegiado:"
print "\t" + str(len(principales) + len(vitalicios) + len(activos))

# en porcentajes del total de socios
percent_principales = len(principales)*100/total_socios
percent_vitalicios  = len(vitalicios)*100/total_socios
percent_activos     = len(activos)*100/total_socios

# Tenemos el dinero que recibió cada grupo de socios
print "Dinero recibido por socios principales: " + str(princi_money)
print "Dinero recibido por socios vitalicios: " + str(vitali_money)
print "Dinero recibido por socios activos: " + str(activo_money)

print "\nPorcentaje de socios con voto privilegiado:"
print "\t" + str(percent_principales + percent_vitalicios + percent_activos)

print "\nPorcentaje del dinero que se recibe este grupo:"
percent_money_pva = (princi_money + vitali_money + activo_money)*100/total_money
print "\t" + str(percent_money_pva)

# Save to CSV file
f = open("output/socios_pva_versus_total.csv", "w")
f.write("socios_pva," + str(percent_principales + percent_vitalicios + percent_activos))
f.write("\nresto_de_socios," + str(100 - percent_principales - percent_vitalicios - percent_activos))
f.write("\nsocios principales vitalicios y activos," + str(percent_money_pva))
f.write("\nresto de socios," + str(100 - percent_money_pva) + "\n")
f.close()

print "Datos se han guardado en archivo ``output/socios_pva_versus_total.csv``"


