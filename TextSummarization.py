import re
import heapq
import nltk
import pandas as pd
import math

# nltk.download('punkt')
# nltk.download('stopwords')

# Read comment from CSV file
path = 'C:\\Users\\Tanachart\\Desktop\\AsianFacts\\dataset_with_like\\'
filename = "1_Population.csv"
dataset = pd.read_csv(path + filename, header=None)
commentList = dataset[0]
likeList = dataset[1]

article_text = ' '.join(commentList)

# Removing Square Brackets and Extra Spaces
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)
article_text = re.sub(r'\"', ' ', article_text)

# Removing special characters and digits
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

# Return a sentence-tokenized copy of *text*,
# using NLTK's recommended sentence tokenizer
sentence_list = nltk.sent_tokenize(article_text)

# print("original text")
# print(article_text)
# print("Sentence Segmentation")
# print(sentence_list)
# print("Word Tokenization")
# print(nltk.word_tokenize(formatted_article_text))
# Get list of stopword
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

# Calculating Sentence Scores
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

print("Default score")
print(sentence_scores)

print("\nlike score")
for i in range(len(commentList)):
    for j in range(len(list(sentence_scores.keys()))):
        if list(sentence_scores.keys())[j] in commentList[i]:
            likeWeight = (likeList[i] / sum(likeList)) * list(sentence_scores.values())[j]
            if not math.isnan(likeWeight):
                print(likeWeight)
                newValue = list(sentence_scores.values())[j] + likeWeight
                sentence_scores[list(sentence_scores.keys())[j]] = newValue

print("\nSum with like")
print(sentence_scores)

print('number of all sentences : '+str(len(sentence_list)))
inputNumber = input("Enter number of sentences (%) : ")

if int(inputNumber) > 100:
    inputNumber = 100

numberOfLine = round((int(inputNumber) * len(sentence_list))/100)
if numberOfLine < 1:
    numberOfLine = 1

# # Calculate number of line to be display after summarization
# numberOfLine = round(len(nltk.word_tokenize(formatted_article_text)) / 100)
# if numberOfLine > 3:
#     numberOfLine = 3

summary_sentences = heapq.nlargest(numberOfLine, sentence_scores, key=sentence_scores.get)

print("\n")
print(filename)
print("========== ORIGINAL SENTENCES ==========")
print(sentence_list)
print('Number of words : ' + str(len(nltk.word_tokenize(formatted_article_text))))
summary = ' '.join(summary_sentences)
print("========== SUMMARY SENTENCES ==========")
print(summary)
print('Number of sentences : ' + str(numberOfLine))
