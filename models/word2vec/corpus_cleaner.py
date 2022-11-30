#!/usr/bin/env python
# coding: utf-8

# # importing the libraries 

# In[2]:


import os 
import re


# In[7]:


input_dir='../../abp_news_hindi_data/train/pos'
all_files_list = os.listdir(input_dir)
for i in range(len(all_files_list)):
    all_files_list[i]='../../abp_news_hindi_data/train/pos/' +all_files_list[i]


# In[8]:


f= open('../final_stopwords.txt', 'r')
stop_words = f.read()
stop_words=stop_words.split("\n")

def clean_file(filename):
    f= open(filename, 'r')
    file_data=f.read()
    f.close()
    cleaned_data= re.sub('[A-Za-z]', "" , file_data)
    cleaned_data = re.sub('[0-9]', "" , cleaned_data)
    # cleaned_data = re.sub('.', "" , cleaned_data)
    
    cleaned_data =cleaned_data.replace("...",".")
    cleaned_data = re.sub(' +', " " , cleaned_data)
    cleaned_data = re.sub('\t', " " , cleaned_data)
    disallowed_characters = "_\,“-\"।–()@#$%&*/‘\'’|\:\”"
    for character in disallowed_characters:
	    cleaned_data = cleaned_data.replace(character, "")
    cleaned_data = re.sub(' +', " " , cleaned_data)
    cleaned_data = re.sub('\t', " " , cleaned_data)
    cleaned_data = re.sub("\!" ,'\n',cleaned_data)
    cleaned_data = re.sub("\." ,'.\n',cleaned_data)
    cleaned_data = re.sub("\?" ,'\n',cleaned_data)
    # cleaned_data = re.sub("\n" ,'\n',cleaned_data)
    cleaned_data = cleaned_data.split('\n')
    new_cleaned_data =[]
    for data in cleaned_data:
        if data is not None and len(data)>=5:
            new_cleaned_data.append(data)   
    
    data_in_string= ""
    for data in new_cleaned_data:
        data_in_string+=data
        data_in_string+='\n'
    return data_in_string
    
    
def clean_2(file_path):
    f= open(file_path, 'r')
    data= f.read()
    data = data.split('\n')
    for i in range(len(data)):
        data[i] = data[i].strip()
        data[i]=re.sub('\[\]',"",data[i])
        data[i]=data[i].split(' ')
        
           
        
    data_in_string= ""
    for data_list in data:
        for data_word in data_list:
            if data_word is not None and data_word not in stop_words:
                data_in_string+=data_word.strip()
                data_in_string+=' '
        data_in_string+='\n'
    return data_in_string

i=0
path='../../abp_news_hindi_data/train/pos/i'
for file_path in all_files_list:
    f = open(file_path,'r')
    data=f.read()
    data=data.split('\n')
    for data_line in data:
        y=open(path +str(i)+'.txt','w')
        i+=1
        y.write(data_line)
        y.close()
    f.close()
    os.remove(file_path)
    
    
        




    
    

