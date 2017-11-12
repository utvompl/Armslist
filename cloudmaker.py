from os import path
import csv
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt 


wordList = []
# read 9th column in data which represents description in all ads
with open('results.csv', 'r', encoding="utf8") as f:
    reader = csv.reader(f)
    wordlist = '\t'.join([i[9] for i in reader])

# read mask image

glock = np.array(Image.open("glock.jpg"))

# unwanted words
stopwords = set(STOPWORDS)
stopwords.add("Â")


wordcloud = WordCloud(max_font_size=40, background_color='black', max_words=200, mask=glock, stopwords=stopwords, width=2280, height=2280).generate(wordlist)

wordcloud.to_file("glockmap.jpg")

plt.figure(figsize=(57,57))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
