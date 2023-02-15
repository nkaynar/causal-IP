

library(rjson)


setwd("~/Documents/Nur/paper_computationalTest_MSrevision/paper codes/limited length unconflicted/Oracle setting/ASP_oracle_parallel/hyttinen2014uai_ver6/pkg/R")
source('load.R')
loud()

args <- commandArgs(trailingOnly = TRUE)

n <- as.numeric(args[1])
n_part <- as.numeric(args[2])
n_i <- as.numeric(args[3])
n_f <- as.numeric(args[4])


L<- test(4, n, n_i, n_f)

x<- toJSON(global_indeps)
write(x, file=sprintf("export_part%d.JSON", n_part))

