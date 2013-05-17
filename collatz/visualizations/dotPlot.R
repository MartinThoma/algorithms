library(ggplot2)

png("collatz-max-in-seq.png", width = 512, height = 800)

mydata = read.csv("../collatz-maxNumber.csv")

# Prepare data
p<-ggplot(mydata, aes(x=n, y=maximum))+ scale_y_continuous(formatter = "comma", limits = c(0, 100000))

p<-p + geom_point()
#p<-p + geom_hex(bins=50)
p<-p + opts(panel.background = theme_rect(fill='white', colour='white'))

# This will save the result in a pdf file called Rplots.pdf
p

dev.off()

