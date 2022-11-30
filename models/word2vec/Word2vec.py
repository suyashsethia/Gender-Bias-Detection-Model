#!/usr/bin/env python
# coding: utf-8

# In[1]:


from gensim.models import Word2Vec
import os 
from sklearn.decomposition import PCA
import re
from pprint import pprint

import matplotlib.pyplot as pyplot
from matplotlib.pyplot import figure
from matplotlib.font_manager import FontProperties
from wxconv import WXC


# In[ ]:



input_path='/home/turning/Desktop/CL_project/CL_PROJECT_CODE/Kerasmodel/aclImdb/train/pos/'
list_files=[]
for x in os.listdir(input_path):
    if x.endswith(".txt"):
        list_files.append(input_path+x)


corpus=""
cleaned_corpus=""
for file_path in list_files:
	f=open(file_path,'r')
	corpus+=f.read()

corpus = re.sub('▁-', " " , corpus)
corpus = re.sub('[A-Za-z]', "" , corpus)
corpus = re.sub('[0-9]', "" ,corpus)

for x in corpus:
    if x != ',':
        cleaned_corpus+=x

sentences=cleaned_corpus.split("\n")

for i in range(len(sentences)):
    sentences[i]=sentences[i].replace("।","")
    sentences[i]=sentences[i].replace("?","")

    sentences[i]=sentences[i].split()


# In[ ]:



# train model
model = Word2Vec(sentences, min_count=1 ,vector_size=100,sg=1)
# fit a 2d PCA model to the vectors
X = model.wv[model.wv.index_to_key]
pca = PCA(n_components=3)
result = pca.fit_transform(X)
plt_1 = pyplot.figure(figsize=(100, 50))
# create a scatter plot of the projection
con = WXC(order='utf2wx')
pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.index_to_key)
# print(result)
for i, word in enumerate(words):
	pyplot.annotate(con.convert(word), xy=(result[i, 0], result[i, 1]))
pyplot.show()


# In[20]:


print(model.wv['एक'])

