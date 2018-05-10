##########Data_Collection#######################################

f1=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_1995.txt")
f2=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_1996.txt")
f3=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_1997.txt")
f4=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_1998.txt")
f5=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_1999.txt")
f6=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2000.txt")
f7=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2001.txt")
f8=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2002.txt")
f9=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2003.txt")
f10=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2004.txt")
f11=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2005.txt")
f12=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2006.txt")
f13=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2007.txt")
f14=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2008.txt")
f15=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2009.txt")
f16=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2010.txt")
f17=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2011.txt")
f18=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2012.txt")
f19=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2013.txt")
f20=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2014.txt")
f21=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2015.txt")
f22=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2016.txt")
f23=read.delim("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles2/all_2017.txt")


setwd("C:/Users/Owner/Desktop/BIMA Capstone/Final Project/_txtfiles") #folder with only the files that worked

dataset = rbind(f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23)
View(dataset)
dataset=dataset[,-1]
#View(smalldataset)

####################################################################################
library(spotifyr)

colnames(dataset)[11] = "track_uri"

as.character(dataset$track_uri)
dataset$track_uri = substr(dataset$track_uri,15,36)
class(dataset$album_release_date)      
dataset$album_release_date=as.Date(dataset$album_release_date)

dataset = na.omit(dataset)

timeAgo = Sys.Date()-dataset$album_release_date
dataset = data.frame(dataset,timeAgo)

 
Winter = c(12,01,02)
Spring = c(03,04,05)
Summer = c(06,07,08)
Fall = c(09,10,11)

winter = as.numeric(substr(dataset$album_release_date,6,7)) %in% Winter
spring = as.numeric(substr(dataset$album_release_date,6,7)) %in% Spring
summer = as.numeric(substr(dataset$album_release_date,6,7)) %in% Summer
fall = as.numeric(substr(dataset$album_release_date,6,7)) %in% Fall

dataset = data.frame(dataset, winter, spring, summer, fall)
View(dataset)
