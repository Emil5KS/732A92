
maiden <- read.csv2("../data/songs.csv", header = FALSE)

for (row in 1:nrow(maiden)){
  
  if(is.na(maiden[row,4]) & row > 1 ){
    maiden[(row),c(1,3,4)] <- maiden[(row - 1),c(1,3,4)]
  }
  
}

colnames(maiden) <- c("song","composers","album","year")

songs <- unique(maiden[c("song","album","year")])
songs$songsnum <- unique(maiden$songnum)
songs$composer1 <- rep("NA", nrow(songs))
songs$composer2 <- rep("NA", nrow(songs))
songs$composer3 <- rep("NA", nrow(songs))
songs$composer4 <- rep("NA", nrow(songs))


maiden$songnum <- as.numeric(maiden$song)

i <- 1
for (song in unique(maiden$songnum) ){
  
  composers <- as.character(maiden$composer[maiden$songnum == song])
  print(composers)
  
  if(length(composers) == 1){
    songs$composer1[i] <- composers
  }
  
  if(length(composers) == 2){
    songs$composer1[i] <- composers[1]
    songs$composer2[i] <- composers[2]
    
  }
  
  if(length(composers) == 3){
    songs$composer1[i] <- composers[1]
    songs$composer2[i] <- composers[2]
    songs$composer3[i] <- composers[3]
    
  }
  
  if(length(composers) == 4){
    songs$composer1[i] <- composers[1]
    songs$composer2[i] <- composers[2]
    songs$composer3[i] <- composers[3]
    songs$composer4[i] <- composers[4]
    
  }
  
  
  i <- i + 1
}




substrRight(songs$song[100])

songs$song <- as.character(songs$song)
songs$song[87] <- "Montsegur" 


songs$song <- as.character(sub("\\[.*\\]",replacement ="", songs$song))




substrRight <- function(x){
  x <- as.character(x)
  substr(x, start = 2, stop = nchar(x)-1)
}

for (i in 1:nrow(songs)){
  #print(substrRight(songs$song[i]))
  songs$song[i]<- substrRight(songs$song[i])

}

write.csv(songs, file = "songs_list.csv", row.names = FALSE)
