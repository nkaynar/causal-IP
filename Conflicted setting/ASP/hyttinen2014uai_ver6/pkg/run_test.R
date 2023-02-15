

library(rjson)


setwd("~/Documents/Nur/ASP/hyttinen2014uai_ver6/pkg/R")
source('load.R')
loud()

args <- commandArgs(trailingOnly = TRUE)

n <- as.numeric(args[1])
L<- test(1,n)

x<- toJSON(global_indeps)
write(x, file="export.JSON")


fileConn<-file("solving_time.txt")
write(as.numeric(L[[2]]$solving_time), fileConn)
close(fileConn)

fileConn2 <-file("objective.txt")
write(as.numeric(L[[2]]$objective), fileConn2)
close(fileConn2)

fileConn3 <-file("true_D.csv")
write.csv(L[[1]]$G, fileConn3)



fileConn4 <-file("true_E.csv")
write.csv(L[[1]]$Ge, fileConn4)
#close(fileConn4)


fileConn5 <-file("est_D.csv")
write.csv(L[[2]]$G, fileConn5)



fileConn6 <-file("est_E.csv")
write.csv(L[[2]]$Ge, fileConn6)









