#!/usr/bin/env python
# coding: utf-8

# # making data dictionaries

# In[11]:


#making the dictionaries of the data 

vectors_file= open('abp_trained/vectors.tsv','r') 
# vectors of all words in metadata these are the already calculated vectors using this repository code

vector_dict = {}
with open('abp_trained/metadata.tsv','r') as words_file:
    for line in words_file:
        vector= vectors_file.readline().split('\t')
        vector_dict.update({line.strip('\n'):vector})


# # making dictionaries for attributes 

# In[12]:


# creating different dict for weat 
import os

path = '../../attribute_list_hindi' #path to file containing the list of attributes

file_list_new = os.listdir(path)
file_list=[]
for i in range(len(file_list_new)):
    file_list.append(path+'/'+file_list_new[i])
weat_dict={}
for j , files in enumerate(file_list):
    f = open(files,'r')
    old_data = f.read().split('\n')
    data=[]
    for i in old_data:
        if i != '':
            data.append(i)
    
    weat_dict.update({file_list_new[j].replace(".txt",""):data})
    
    
    


# # Calculating the distances 
# ## between attributes of different domain with male and female vectors

# In[14]:


import math 

def eu_dist(v1, v2):
    '''
    Calculates distances betweeen 2 vectors. 
    dimensions must be same.
    Arguments : v1(list)  , v2(list)
    Returns  : (list)result
    '''
    dist=0
    for i in range(len(v1)):
        dist+=((v1[i] -v2[i])**2)
    dist= math.sqrt(dist)
    return dist

def add_list(l1, l2):
    '''
    adds two list such that result[i]= l1[i]+l2[i]
    Arguments : l1(list)  , l2(list)
    Returns  : (list)result
    
    '''
    result=[]
    if len(l1)==0:
        return l2
    for i in range(len(l2)):
        result.append(float(l1[i])+float(l2[i]))
    return result


average_dict={} # dictionary containing averages of all attributes

for key , values in weat_dict.items():
    i =0
    average_vec=[]
    
    for value in values :
        
        try:      
            average_vec=add_list(average_vec, vector_dict[value])
            i+=1
           
        except :
            pass
    
    for j in range(len(average_vec)):
        average_vec[j]=average_vec[j]/i
        # print(type(average_vec[j]))
        
    average_dict.update({key:average_vec })
    
    

            
        
    
        


# # Calculating Male/Female Distance ratio 

# In[15]:


eu_dist_dict={}
co_dist_dict={}

male_vect= average_dict['male_terms_hindi']
female_vect= average_dict['female_terms_hindi']

for key in average_dict.keys():
    if key =="male_terms_hindi" or key =='female_terms_hindi':
        continue
    male_dist= eu_dist(male_vect , average_dict[key])
    female_dist= eu_dist(female_vect , average_dict[key])
    
    bias_ratio=male_dist/female_dist
    eu_dist_dict.update({key:bias_ratio})
    
    
from scipy import spatial
for key in average_dict.keys():
    if key =="male_terms_hindi" or key =='female_terms_hindi':
        continue
    male_dist = 1 - spatial.distance.cosine(male_vect,average_dict[key])
    female_dist= 1 - spatial.distance.cosine(female_vect,average_dict[key])
    bias_ratio=male_dist/female_dist
    co_dist_dict.update({key:bias_ratio})


# In[1]:


eu_dist_dict

