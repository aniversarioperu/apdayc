SRC = $(wildcard *.md)

DOCS = $(SRC:.md=.docx)
PDFS = $(SRC:.md=.pdf)

doc: clean $(DOCS)

pdf: clean $(PDFS)

%.docx: %.md refs.bib
	pandoc -f markdown -V geometry:margin=1in -t docx $< --bibliography=refs.bib -o $@

%.pdf: %.md header.latex refs.bib
	pandoc --latex-engine=xelatex -s -S --template header.latex -f markdown -V geometry:margin=1in $< --bibliography=refs.bib -o $@

	

clean:
	rm -rf *pdf *docx
	rm -rf tmp* all_data.csv
	rm -rf output/*png output/socios_pva_versus_total.csv

analysis: all_data.csv top20.png top10.png output/mas_productivos.png output/mas_productivos_apdayc_2012.csv output/socios_pva_versus_total.png
	
all_data.csv: data/*txt
	ls data/*txt | egrep '/[0-9]{2}\.txt' | xargs cat > $@

top20.png: all_data.csv code/plot.py
	cat all_data.csv | awk -F ',' '{print $$2}' | sort | uniq -c | sort -hr | sed 's/^\s\+//g' | grep -v '1 ' | sed -r 's/^([0-9]+)\s+/\1,/g' > tmp
	python code/plot.py
	

top10.png: all_data.csv
	python code/top10.py


output/mas_productivos.png: tmp_mas_productivos.txt

output/mas_productivos_apdayc_2012.csv tmp_mas_productivos.txt: data/mas_productivos_2012.txt code/mas_productivos.py data/socios_principales.tsv
	cat data/mas_productivos_2012.txt | sed 's/S\/\.//g' | sed 's/\$$//g' | sed 's/\s\+/ /g' | sed -r 's/([A-Z]),/\1/g' | sed 's/,//g' | sed -r 's/(([A-Z]+\s)+)/\1,/g' | sed 's/ ,/,/g' | sed -r 's/^[0-9]+\s[0-9]+\s//g' | sed -r 's/\s*$$//g' > tmp_mas_productivos.txt
	echo "Nombre Socio,Ejecucion,Radio y TV,Fono-Mecanico,Contingencia,Jingles,Cable,Copia Privada,DSP,TOP 100 Dial,Top 5000,Total,Extranjero,TOTAL PRODUCIDO" > output/mas_productivos_apdayc_2012.csv
	cat tmp_mas_productivos.txt | sed -r 's/([0-9])\s([0-9])/\1,\2/g' >> output/mas_productivos_apdayc_2012.csv
	python code/mas_productivos.py


socios_principales: output/socios_principales.png output/socios_principales_vitalicios_activos.png output/socios_pva_versus_total.png
	
output/socios_pva_versus_total.csv output/socios_principales.png output/socios_principales_vitalicios_activos.png: data/socios_principales.txt output/tmp_socios_principales.txt code/plot_socios_principales.py
	python code/plot_socios_principales.py 8000

output/tmp_socios_principales.txt:
	cat data/socios_principales.txt | sed 1d | sed 's/,//g' | cut -c 32-200 | sed -r 's/\s{2,}/,/g' > output/tmp_socios_principales.txt

output/socios_pva_versus_total.png: output/socios_pva_versus_total.csv code/plot_socios_principales.py output/tmp_socios_principales.txt code/plot_socios_pva_versus_total.R
	R --no-save < code/plot_socios_pva_versus_total.R

# Cuantos socios tiene APDAYC? 8mil?
# Podemos intentar estimar cuantos socios deberia tener.
# Tenemos las ganancias de los 250 socios más prolificos. Y tenemos la cantidad
# total de regalias que se repartieron en el 2012. Podemos ajustar un modelo
# estadístico de distribucion de datos y ver cuantos socios son necesarios para
# distribuir 29 millones de soles.
fit_distribution: tmp_mas_productivos.txt
	echo "Ejecucion,RadioTv,Fono-mecanico,Contingencia,Jingles,Cable,CopiaPrivada,DSP,Top100,Top5000,Total,Extranjero,TotalProducido" > output/ganancias_top_250.csv
	cat tmp_mas_productivos.txt | awk -F ',' '{print $$2}' | sed -r 's/\s+/,/g' >> output/ganancias_top_250.csv
