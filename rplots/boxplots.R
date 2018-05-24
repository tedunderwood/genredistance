# horizontal boxplot

with = scan('/Users/tunder/Dropbox/python/genres/results/bootstrapped_topicwith_r.txt')
tfidf = scan('/Users/tunder/Dropbox/python/genres/results/bootstrapped_tfidf_r.txt')
pred = scan('/Users/tunder/Dropbox/python/genres/results/bootstrapped_predictive_r.txt')
sans = scan('/Users/tunder/Dropbox/python/genres/results/bootstrapped_topicsans_r.txt')
normed = scan('/Users/tunder/Dropbox/python/genres/results/bootstrapped_topicdatenormed.txt')

medians = c(-tfidf[5000], -sans[5000], -with[5000], -normed[5000], pred[5000])
lower = c(-tfidf[250], -sans[250], -with[250], -normed[250], pred[250])
upper = c(-tfidf[9750], -sans[9750], -with[9750], -normed[9750], pred[9750])

data = data.frame(ymin = lower, ymax = upper, med = medians, 
                  method = as.factor(c('tfidf word\nvectors', 
                             'topic vectors for non-\noverlapping genres',
                             'topic vectors for\noverlapping genres',
                             'topic vectors\nadjusted for date', 
                             'correlations between\npredictive models')))

data$method = factor(data$method, 
                     levels = c("tfidf word\nvectors", 
                                "topic vectors for non-\noverlapping genres", 
                                "topic vectors for\noverlapping genres", 
                                "topic vectors\nadjusted for date", 
                                'correlations between\npredictive models'),
                     ordered = TRUE)

library(ggplot2)

p <- ggplot(data, aes(x = method, ymin = ymin, ymax = ymax, med = med, color = method)) +
  geom_errorbar(aes(x = method, ymin = ymin, ymax = ymax), width = 0.5, size = 1) + geom_point(aes(x= method, y = med), size=4, shape=21, fill="white") + 
  coord_flip() + scale_colour_brewer(palette = 'Dark2') +
  scale_y_continuous(limits = c(0, 0.6)) +
  labs(y = '\ncorrelation with social evidence of genre proximity', x = '') +
  theme(legend.position="none",
        text = element_text(size = 16, family = "Avenir Next Medium"))

tiff("/Users/tunder/Dropbox/python/genres/images/boxplots.tiff", height = 4, width = 9, units = 'in', res=400)
plot(p)
dev.off()
plot(p)