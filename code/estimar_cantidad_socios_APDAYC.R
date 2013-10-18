library(ggplot2)
library(fitdistrplus)

x <- read.csv("output/ganancias_top_250.csv")

# extraer los totales recaudados, que están como "Total Producido"

totales <- x$TotalProducido

