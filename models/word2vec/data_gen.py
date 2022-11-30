#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import html5lib 


# In[2]:


page = requests.get('https://www.abplive.com/') # Getting page HTML through request
soup = BeautifulSoup(page.content, 'html5lib') 


# In[6]:


all_links = set()
links1=set()
links2=set()
for link in soup.findAll('a'):
  if link.get("href") and link.get('href').startswith('https://www.abplive.com/') :
    links1.add(link.get('href'))
    all_links.add(link.get('href'))

for urls in links1:
  page = requests.get(urls) # Getting page HTML through request
  soup = BeautifulSoup(page.content, features="xml") 
  for link in soup.findAll('a'):
    link_url= link.get('href')
    if link_url :
      if  link_url.startswith('https://www.abplive.com/') and link_url not in all_links :
        links2.add(link.get('href'))
        all_links.add(link.get('href'))
links1=set()
for urls in list(links2): 
    flg=1
    page = requests.get(urls) # Getting page HTML through request
    soup = BeautifulSoup(page.content, features="xml") 
    for link in soup.findAll('a'):
     link_url= link.get('href')
     if link_url :
      if link_url.startswith('https://www.abplive.com/') :
        all_links.add(link_url)
      if len(all_links)>10000:
        flg=0
        break
    if flg==0 :
      break;


# In[2]:


all_links=[]
with open('output','r') as f:
    for line in f:
        all_links.append(line.replace('\n',''))


# In[4]:


all_links=[]
with open('output','r')as f:
    for line in f:
        all_links.append(line.replace("\n",""))


# In[9]:


news_corpus = ""
string= "/home/turning/Desktop/CL_FINAL_PROJECT/abp_news_hindi_data/train/pos/in"

for i, url in enumerate(all_links):
  
  try:
    req = requests.get(url)
    html_content = req.content
    soup = BeautifulSoup(html_content, 'html5lib')
    news_corpus_set = soup.find_all('p')
    news_corpus=""
    for element in news_corpus_set:
      news_corpus += element.text
    
    path_file=string+str(i%100)+'.txt'
    
    f = open(path_file,'a')
    
    f.write(str(news_corpus))
    f.close()
  except:
    pass


# In[ ]:


links2=set()

for urls in all_links:
    if 'topic' in urls:
        page = requests.get(urls) # Getting page HTML through request
        soup = BeautifulSoup(page.content, features="xml") 
        for link in soup.findAll('a'):
            link_url= link.get('href')
            if link_url :
                if  link_url.startswith('https://www.abplive.com/') and link_url not in all_links :
                    links2.add(link.get('href'))
                    # all_links.add(link.get('href'))
            

