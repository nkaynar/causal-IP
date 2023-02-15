

library(rjson)


setwd("~/Documents/Nur/ASP_run/hyttinen2014uai_ver6/pkg/R")
source('load.R')
loud()

args <- commandArgs(trailingOnly = TRUE)

n <- as.numeric(args[1])

L<- test(4,n)

x<- toJSON(global_indeps)
write(x, file="export.JSON")

fileConn<-file("solving_time_oldsat.txt")
write(as.numeric(L$solving_time), fileConn)
close(fileConn)

