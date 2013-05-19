library(ggplot2)

mydata = read.csv("../collatz-maxNumber.csv")

# Prepare data
p<-ggplot(mydata, aes(x=n, y=maximum, color=factor(steps, each=10)))+ scale_y_continuous(formatter = "comma", limits = c(0, 100000))+ scale_x_continuous(formatter = "comma", limits = c(0, 10000))

p<-p + geom_point()
#p<-p + geom_hex(bins=50)
p<-p + opts(panel.background = theme_rect(fill='white', colour='white'))

# This will save the result in a pdf file called Rplots.pdf
#p

ggsave(file="collatz-sequence-and-steps-for-n.pdf")
#ggsave(file="collatz-sequence-and-steps-for-n.png")
