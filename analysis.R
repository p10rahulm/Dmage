library(stringr)


rawread <- read.csv("rawdata/categories.txt",na.strings = F,stringsAsFactors = F)
rawread <- unlist(rawread)
transactions.list <- data.frame(transaction.contents = rawread)
row.names(transactions.list) <- 1:nrow(transactions.list)
transactions.list$transaction.id <- paste0("T",1:nrow(transactions.list))
rm(rawread)
transactions.list$transaction.contents <- as.character(transactions.list$transaction.contents)
write.csv(transactions.list,"rawdata/transactions_list.csv")

categories <- strsplit(transactions.list$transaction.contents[1], ";", fixed = FALSE, perl = FALSE, useBytes = FALSE)[[1]]
i=2
for (i in 2:nrow(transactions.list)){
  categories <- c(categories,strsplit(transactions.list$transaction.contents[i], ";", fixed = FALSE, perl = FALSE, useBytes = FALSE)[[1]])
}
categories <- as.data.frame(categories)
names(categories) <- "category.name"




# categories$category.name <- as.factor(categories$category.name)
categories.L1.freq <- as.data.frame(sort(table(categories$category.name),decreasing = T))
names(categories.L1.freq) <- c("category.name",'frequency')
categories.L1.freq$category.name <- as.character(categories.L1.freq$category.name)


rm(categories,i)
frequent.categories <- categories.L1.freq[categories.L1.freq$frequency>771,]
frequent.categories$level <- 1
frequent.categories$outputformat <- paste0(frequent.categories$frequency,":",frequent.categories$category.name)
write(frequent.categories$outputformat,"output/patterns.txt")
rm(categories.L1.freq)

l2cat <- t(combn(frequent.categories$category.name, 2))
l2cat <- data.frame(cat1 = l2cat[1:dim(l2cat)[1],1],cat2 = l2cat[1:dim(l2cat)[1],2])
#Converting to character vector
# l2cat <- data.frame(lapply(l2cat, as.character), stringsAsFactors=FALSE)

l2cat$numocc <- 0
for(i in 1:nrow(l2cat)){
  l2cat$numocc[i] <- l2cat$numocc[i] + sum(grepl(l2cat$cat1[i],transactions.list$transaction.contents) & grepl(l2cat$cat2[i],transactions.list$transaction.contents))
}
rm(i)
l2cat <- l2cat[order(l2cat$numocc,decreasing = T),]
rownames(l2cat) <- 1:nrow(l2cat)
l2cat <- l2cat[l2cat$numocc>771,]












# Generating generality
cat.prev <- l2cat
for(i in 1:nrow(cat.prev)){
  
  cat.prev$sumstring[i] <- paste(sort(cat.prev[i,!names(cat.prev) %in% c("numocc","sumstring")]),collapse = ";")  
}
rm(i)
cat.prev$sumstring <- paste0(cat.prev$numocc,":",cat.prev$sumstring)









# Get unique categories still left over in string
uniques <- as.character(unique(unlist(cat.prev[,!names(cat.prev) %in% c("numocc","sumstring")],use.names = F)))
cat.combs <- t(combn(uniques, 3))
cat.combs <- as.data.frame(cat.combs)
# cat.combs <- data.frame(lapply(cat.combs, as.character), stringsAsFactors=FALSE)

cat.combs.true.false <- data.frame(filtered = rep(F,nrow(cat.combs)))
                                   
for(catcombrow in 1:nrow(cat.combs)){
  sumnrowchk = 0
  for (nrows in 1:3) {
    elements  <-  t(combn(cat.combs[catcombrow,],2))[nrows,]
    elements <-  sort(unlist(elements))
    elements <- paste(elements,collapse = ";")
    # print(elements)
    mysum = 0
    if(sum(grepl(elements,cat.prev$sumstring))>=1){mysum = 1}
    # print(mysum)
    sumnrowchk = sumnrowchk + mysum
  }
  if(sumnrowchk >=3){
    cat.combs.true.false[catcombrow,] <- T
  }
}

cat.combs <- cbind(cat.combs,cat.combs.true.false)
cat.combs <- cat.combs[cat.combs$filtered==T,]
cat.combs <- cat.combs[,!names(cat.combs) %in% c("filtered")]

# Check for occurances in main transaction db

cat.combs$numocc <- 0
for(i in 1:nrow(cat.combs)){
    cat.combs$numocc[i] <- cat.combs$numocc[i] + sum(grepl(cat.combs[i,1],transactions.list$transaction.contents) & grepl(cat.combs[i,2],transactions.list$transaction.contents) & grepl(cat.combs[i,3],transactions.list$transaction.contents))

}
rm(i)
cat.combs <- data.frame(lapply(cat.combs, as.character), stringsAsFactors=FALSE)

# some temporary fixes
tempcat <- cat.combs
tempcat <- tempcat[!grepl("Food",tempcat[,1]),]
tempcat <- tempcat[!grepl("Food",tempcat[,2]),]
tempcat <- tempcat[!grepl("Food",tempcat[,3]),]
tempcat <- tempcat[order(tempcat$numocc,decreasing = T),]

for(i in 1:nrow(tempcat)){
  
  tempcat$sumstring[i] <- paste(sort(tempcat[i,!names(tempcat) %in% c("numocc","sumstring")]),collapse = ";")  
}
rm(i)
tempcat$sumstring <- paste0(tempcat$numocc,":",tempcat$sumstring)


tempcat <- cat.combs
tempcat <- tempcat[order(tempcat$numocc,decreasing = T),]

for(i in 1:nrow(tempcat)){
  
  tempcat$sumstring[i] <- paste(sort(tempcat[i,!names(tempcat) %in% c("numocc","sumstring")]),collapse = ";")  
}
rm(i)
tempcat$sumstring <- paste0(tempcat$numocc,":",tempcat$sumstring)




































