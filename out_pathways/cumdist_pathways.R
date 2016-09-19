#!/usr/bin/Rscript

# args <- commandArgs(True)
# 
# ## Default setting when no arguments passed
# if(length(args) < 1) {
#   args <- c("--help")
# }
# 
# ## Help section
# if("--help" %in% args) {
#   cat("
#       Help: cumdist_pathways.R
#  
#       Arguments:
#       --arg1=someValue   - numeric, blah blah
#       --arg2=someValue   - character, blah blah
#       --arg3=someValue   - logical, blah blah
#       --help              - print this text
#  
#       Example:
#       ./test.R --arg1=1 --arg2="output.txt" --arg3=TRUE \n\n")
#   
#   q(save="no")
# }

setwd("~/Documents/Stanford Coterm Year/ICME Research/pathways_project/out_pathways")

library(dplyr)
library(reshape2)
library(ggplot2)
theme_set(theme_bw())

paths <- read.table("pathways_ecoevo_sub.txt", sep="\t", header=FALSE, stringsAsFactors=FALSE)

splitcols <- apply(paths,2,strsplit,',')
n_years <- length(splitcols)

course_long <- matrix(nrow = 0, ncol=2)
for(i in 1:n_years) {
  unlisted <- unlist(splitcols[i])
  n_rows <- length(unlisted)
  add_to_long <- data.frame(rep(i, n_rows), unlisted)
  course_long <- rbind(course_long, add_to_long)
}
colnames(course_long) <- c("qtr","course")

course_counts <- table(course_long)
course_sums <- colSums(course_counts)
course_props <- apply(course_counts, 1, function(x) {x / course_sums})
course_cumsums <- apply(course_props, 1, cumsum)

course_cumsums_long <- melt(course_cumsums)
colnames(course_cumsums_long) <- c("qtr","course","cumsum")

p1 <- ggplot(course_cumsums_long, aes(x=qtr, y=cumsum, col=course)) + geom_line()
ggsave("cumsum_plot.png", p1, device="png")
X11()
plot.new()
p1
locator(1)