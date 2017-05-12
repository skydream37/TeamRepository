library(rjson)
setwd("~/Desktop/TeamRepository/data")
alljsonData <- fromJSON(file = "all_langs.json")
#alljsonData #是list

#建立有兩欄空值的矩陣，要把語言和數量放進去
mat = matrix(rep(0, length(alljsonData)*2), nrow=length(alljsonData))
#mat

i = c(1)
for (name in names(alljsonData)){
  mat[i,1] = name
  mat[i,2] = alljsonData[[name]]
  i = i + c(1)
}
#mat

#把mat轉成dataframe
df = as.data.frame((mat))
#把字串轉成數值 不要放回mat[,2]他會又轉成cha不知為何
a = as.numeric(mat[,2])


#畫圓餅圖
pct = round(a/sum(a)*100,1)
labels = paste(mat[,1],pct,"%")
pie(a,labels = labels)


#畫長條圖
barplot(a)
barplot(a,main = "Hot Languages",names.arg = mat[,1],las=2)