library(ggplot2)

mydata = read.csv("/home/moose/Downloads/algorithms/collatz/steps.csv")

# Prepare data
p<-ggplot(mydata, aes ( x=n,y=steps ))

p<-p + geom_hex(bins=30)
p<-p + opts(panel.background = theme_rect(fill='white', colour='white'))

# This will save the result in a pdf file called Rplots.pdf
p
