library(ggplot2)
library(ggrepel)

gdata <- read.csv('/Users/tunder/Dropbox/python/genres/results/predictivetopicmap.tsv', sep = '\t')

tocut = c('Subj: Short stories, American', 'Subj: Short stories, Other', 
         'Subj: SF, American', 'Subj: SF, Other', 'Subj: Man-woman', 'Political')

cutindexes = c()
for (tc in tocut){
  a = which(tc == gdata$genre)
  cutindexes = c(cutindexes, a)
}

gdata = gdata[-cutindexes, ]

p <- ggplot(gdata, aes(x = xcord, y = ycord, color = meandate)) +
  geom_point(alpha = 0.7, size = 3) + theme_bw() +
  labs(x = '', y = '') +
  geom_text_repel(aes(xcord, ycord, label = genre), force = 4.4, box.padding = 0.25, 
                  point.padding = 0.3, max.iter = 300, size = 5,
                  family = "Avenir Next Medium") +
  theme(axis.title.x=element_blank(),
        axis.text.x=element_blank(),
        axis.ticks.x=element_blank(),
        axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        )

tiff('/Users/tunder/Dropbox/python/genres/images/predictivetopicmap.tiff', height = 8, width = 8, units = 'in', res=400)
plot(p)
dev.off()
plot(p)