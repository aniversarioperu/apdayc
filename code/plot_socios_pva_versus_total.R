library(ggplot2)
datos <- read.csv("output/socios_pva_versus_total.csv", sep=",",
              header=FALSE)
money <- datos[3:4,]
names(money) <- c("Socios","Regalías")

png(filename="output/socios_pva_versus_total.png",
      width=950, height=630, units="px")
ggplot(money, aes(x="", y=Regalías, fill=Socios)) +
  theme(text = element_text(size=22)) +
  geom_bar(width=1, stat="identity") +
  coord_polar("y", start=pi/3) +
  labs(title="Repartición de regalías, APDAYC 2012")
dev.off()