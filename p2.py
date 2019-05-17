


text = """

"Last couple years ago I did a wine tour with my family in Cyprus. I can tell you this, Cyprus truly is a wine country. This island also has exceptionally stunning scenery. The locals here are very nice and welcoming. I suggest to come by during September, because Sep. is traditional month of the grape harvest from the vineyards covering the rolling slopes of Cyprus. A wine lover?, believe me, you will be blown away.

I just have known that Cyprus has such a contribution in the beverage history. This fact really surprise me since I never tried the wine from Cyprus not have heard about it before, does it just pop up and died in the history or does it just pass the brewery knowledge to other country."

"""


from nltk.tokenize import sent_tokenize, word_tokenize
import sys

# read text file 
#text = '' #create a empty string
#for line in sys.stdin:
#    text = text + line

punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

# convert some odd puncations which can't be recognized by NLTK
text = text.replace('“','"')
text = text.replace('”','"')
text = text.replace("’","'")

# this is stopwords of english from NLTK
sw = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn']

"""
Words that have a frequency term lower than min_cut or higher than max_cut will be ignored.
"""
min_cut = 0.1
max_cut = 0.9
stopwords = set(sw+list(punctuation)+list("it's"))
    
    
"""
Tokenize sentences and words
"""
sents = sent_tokenize(text)
word_sent = [word_tokenize(s.lower()) for s in sents]

"""
Computer the frequency of each of word.
"""
freq = dict()
for s in word_sent:
    for word in s:
        if word not in stopwords:
            if word not in freq:
                freq[word] = 1
            else:
                freq[word] += 1
# frequencies normalization and filerting
m = float(max(freq.values()))
for w in list(freq):
    freq[w] = freq[w]/m
    if freq[w] >= max_cut or freq[w] <= min_cut or w <= "a":
        del freq[w]

ranking = dict()
for i, sent in enumerate(word_sent):
    for w in sent:
        if w in freq:
            if i not in ranking:
                ranking[i] = freq[w]
            else:
                ranking[i] += freq[w]
if 0 in ranking:
    del ranking[0]
textLenReq = len(text.split())*0.25
# sort sentences according to their values
ranking = sorted(ranking,key=ranking.get,reverse=True)


print('----------------------------------')
print('Summary:\n')

# print the first sentence, which is usually important
print('*')
print(sents[0])
textLenReq -= len(sents[0].split())

# print sentences in accordance with their values, as long as the output length is less than 500 or 25% of total text length
outputLen = 0
i = 0
while outputLen < textLenReq and outputLen < 500:
    print('*')
    print(sents[ranking[i]])
    i += 1
    outputLen += len(sents[ranking[i]].split())
