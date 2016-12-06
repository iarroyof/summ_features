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
  labx = ""
  #labx = "Annotator / summarizer"
  
  par(mfrow=c(1,1)) # 
  plotCI(Summarizer, Medians, ui = upsMn, li = dwsMn, ylab = "", xlab = "", axes = F, scol = "blue", 
         slty = "dotted", pt.bg = par("bg"), pch = 19)
  par(mfrow=c(1,1), new=T)
  plotCI(Summarizer, Means, ui = upsMn, li = dwsMn, 
         #main = paste("Statistics for feature [", Name, "] in Baseline and SOA sumarizers"),
         #main = paste("Statistics for feature [", Name, "] in human sumaries"),
         main = paste("Statistics for feature [", Name, "] in human and machine sumaries"),
         ylab = "Feature frequency", xlab = labx, xaxt = 'n')
  axis(1, at=1:length(syss), labels=syss, las=2)
  
}

plot_feature <- function(file, feat){
  grepy0 <- "d30002t."
  grepy1 <- "*d30002t."
  
  data <- read.csv(file)
  names <- data[, 1]
  #names <- subset(data, grepl(grepy0, data[,1]) )[,1]
  feat <- colnames(data)[feat]
  nDocs <- 25 #length(subset(data, grepl(".DPP", data[,1]) )[,1])
  #systems <- list()
  print(paste("Feature name: ", feat))
  
  i <- 1
  syss <- 0
  for (name in names){
    #systems[i] <- sub(grepy1, "", name)
    if (name != ""){
      syss[i] <- substr(name, 8, nchar(name))
      i <- i + 1
    }
  }
  
  systems <- unique(syss)
  
  sys_table <- list()
  i <- 1
  for(sys in systems){
    sys_table[[i]] <- subset(data, grepl(sys, data[,1]) )
    i <- i + 1
  }
  
  syss_feature <- matrix( ,nrow = nDocs, ncol = length(systems))
  i <- 1
  for (sys in sys_table){
    syss_feature[,i] <- sys[,feat][1:nDocs]
    i <- i + 1
  }
  
  get_conf_graph(syss_feature, feat, systems)

}

dir = "/home/iarroyof/R/plots_jir/both_h_nh/"
filin = "DUC04_stat_all_results.csv"
# plot_feature(filin,5)
#plot_feature(filin, 14)
for (p in 2:101){
  png(filename=paste0(dir, "human-nonHuman_25docs_byFeature_", p, ".png"))
  plot_feature(filin, p)
  dev.off()
}

