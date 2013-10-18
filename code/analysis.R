require(ggplot2)
library(vcdExtra)


x <- read.csv("all_data.csv", header=FALSE)
names(x) <- c("rank","cancion")
y <- table(x[,2])
y <- sort(y, decreasing=TRUE)[1:63]

names <- names(y)
barplot(y, las=1, xaxt="n")
axis(1, at=seq(1:63), labels=names, las=2)

c <- ggplot(names(y), aes(as.vector(y)))
c + geom_bar()
