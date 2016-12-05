#!/usr/bin/env Rscript
# R script for computing confidence plot

get_conf_graph <- function(data, Name, syss) {
  r = dim(data)[1]
  c = dim(data)[2]
  ers <- 0
  sds <- 0
  upsMn <- 0
  upsMd <- 0
  dwsMn <- 0
  dwsMd <- 0
  Means <- colMeans(data, na.rm = T)
  Medians <- 0 
  
  for (i in 1:c){
    d <- data[,i] 
    d  <- d[!is.na(d)]
    Medians[i] <- median(as.numeric(as.vector(d)))
    sds[i] <- sd(d)
    ers[i] <- qt(0.975, df=length(d)-1)*sds[i]/sqrt(length(d))
    #dwsMd[i] <- Medians[i] - ers[i]
    #upsMd[i] <- Medians[i] + ers[i]
    dwsMn[i] <- Means[i] - ers[i]
    upsMn[i] <- Means[i] + ers[i]
  }
  
  require(plotrix)
  Summarizer <- 1:c
  
  par(mfrow=c(1,1)) # 
  plotCI(Summarizer, Medians, ui = upsMn, li = dwsMn, ylab = "", xlab = "", axes = F, scol = "blue", 
         slty = "dotted", pt.bg = par("bg"), pch = 19)
  par(mfrow=c(1,1), new=T)
  plotCI(Summarizer, Means, ui = upsMn, li = dwsMn, 
         main = paste("Statistics for feature [", Name, "] in Baseline and SOA sumarizers"), 
         ylab = "Feature frequency", xlab = "", xaxt = 'n')
  axis(1, at=1:length(syss), labels=syss, las=2)
  
}

plot_feature <- function(file, feat){
  #grepy0 <- "d30002t."
  #grepy1 <- "*d30002t."
  grepy0 <- "*T.[:upper:]"
  
  data <- read.csv(file)
  names <- subset(data, grepl(grepy0, data[,1]) )[,1]
  feat <- colnames(data)[feat]
  nDocs <- 25 #length(subset(data, grepl(".DPP", data[,1]) )[,1])
  #systems <- 0
  systems <- list()
  #print(names)

  i <- 1
  for (nam in names){
    #systems[i] <- sub(grepy1, "", nam)
    print(i)
    systems[i] <- substr(nam, 15, 16)
    print(systems[i])
    i <- i + 1
  }
  nSystems <- i - 1

  print(systems)
  
  sys_table <- list()
  i <- 1
  for(sys in systems){
    sys_table[[i]] <- subset(data, grepl(sys, data[,1]) )
    i <- i + 1
  }
  
  syss_feature <- matrix( ,nrow = nDocs, ncol = nSystems)
  i <- 1
  for (sys in sys_table){
    syss_feature[,i] <- sys[,feat][1:nDocs]
    i <- i + 1
  }
  
  get_conf_graph(syss_feature, feat, systems)
  #return(feats)
}

dir="/home/lia/iarroyof/R/plots_jir/non_human/"
# plot_feature("DUC04_stat_results_non_human.csv",5)
plot_feature("DUC04_stat_results_human.csv",5)
#for (p in 2:101){
#  png(filename=paste0(dir,"non_human_25docs_byFeature_", p,".png"))
#  plot_feature("DUC04_stat_results_non_human.csv", p)
#  dev.off()
#}

