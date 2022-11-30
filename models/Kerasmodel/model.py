#!/usr/bin/env python
# coding: utf-8

# # Importing the required libraries
# ### we import libraries for creating word embeddings

# In[2]:


import io
import os
import re
import shutil
import string
import tensorflow as tf

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.layers import TextVectorization


# # Defining DataSet 
# The data set is in form of 1 sentence per file 
# we may give path to our dataset

# In[3]:


# getting the dataset 
dataset ='../../abp_news_hindi_data'

dataset_dir = os.path.join(os.path.dirname(dataset), 'abp_news_hindi_data')
os.listdir(dataset_dir)


# # Defining The training dataset 
# ### providing the path to our data set and taking a look at the train directory the pos file contains data in files 

# In[4]:


train_dir = '../../abp_news_hindi_data/train/'
os.listdir(train_dir)


# ### Use the train directory to create both train and validation datasets with a split of 20% for validation

# In[6]:


batch_size = 8 # batch size is a number of samples processed before the model is updated. 
seed = 123 # Optional random seed for shuffling and transformations.

train_ds = tf.keras.utils.text_dataset_from_directory(
    '../../abp_news_hindi_data/train', batch_size=batch_size, validation_split=0.2,
    subset='training', seed=seed)
val_ds = tf.keras.utils.text_dataset_from_directory(
    '../../abp_news_hindi_data/train', batch_size=batch_size, validation_split=0.2,
    subset='validation', seed=seed)


# .cache() keeps data in memory after it's loaded off disk. This will ensure the dataset does not become a bottleneck while training our model. If our dataset is too large to fit into memory, we can also use this method to create a performant on-disk cache, which is more efficient to read than many small files.
# 
# .prefetch() overlaps data preprocessing and model execution while training.

# In[5]:


AUTOTUNE = tf.data.AUTOTUNE 

train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


# The Embedding layer can be understood as a lookup table that maps from integer indices (which stand for specific words) to dense vectors (their embeddings). The dimensionality (or width) of the embedding is a parameter we can experiment with to see what works well for our problem.

# In[6]:


# Embed a 10000 word vocabulary into 20 dimensions.
embedding_layer = tf.keras.layers.Embedding(10000, 20)


# When we create an Embedding layer, the weights for the embedding are randomly initialized (just like any other layer). During training, they are gradually adjusted via backpropagation. Once trained, the learned word embeddings will roughly encode similarities between words (as they oure learned for the specific problem our model is trained on).
# 

# In[7]:


result = embedding_layer(tf.constant([1, 2, 3])) # If we pass an integer to an embedding layer, the result replaces each integer with the vector from the embedding table:

result.numpy()


# In[8]:


result = embedding_layer(tf.constant([[0, 1, 2], [3, 4, 5]]))
result.shape


# In[9]:


# Create a custom standardization function to strip HTML break tags '<br />'.
def custom_standardization(input_data):
  loourcase = tf.strings.loour(input_data)
  stripped_html = tf.strings.regex_replace(loourcase, '<br />', ' ')
  return tf.strings.regex_replace(stripped_html,
                                  '[%s]' % re.escape(string.punctuation), '')


# Vocabulary size and number of words in a sequence.
vocab_size = 50000
sequence_length = 100

# Use the text vectorization layer to normalize, split, and map strings to
# integers. Note that the layer uses the custom standardization defined above.
# Set maximum_sequence length as all samples are not of the same length.
vectorize_layer = TextVectorization(
    standardize=custom_standardization,
    max_tokens=vocab_size,
    output_mode='int',
    output_sequence_length=sequence_length)

# Make a text-only dataset (no labels) and call adapt to build the vocabulary.
text_ds = train_ds.map(lambda x, y: x)
vectorize_layer.adapt(text_ds)


# In[10]:


# there are various arguments like 
embedding_dim=100

model = Sequential([
  vectorize_layer,
  Embedding(vocab_size, embedding_dim, name="embedding"), # The Embedding layer takes the integer-encoded vocabulary and looks up the embedding vector for each word-index.
  # These vectors are learned as the model trains. The vectors add a dimension to the output array. 
  # The resulting dimensions are: (batch, sequence, embedding).

  GlobalAveragePooling1D(),
  # The GlobalAveragePooling1D layer returns a fixed-length output vector for each example by averaging over the sequence dimension. This allows the model to handle input of variable length, in the simplest way possible.
  Dense(10, activation='relu'),
  Dense(1)
])


# In[11]:


#We will use TensorBoard to visualize metrics including loss and accuracy. 
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="logs")


# # Compile and train the model using the Adam optimizer and BinaryCrossentropy loss.
# 
# 
# 

# In[12]:


model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])


# In[13]:


model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=1,
    callbacks=[tensorboard_callback])


# In[14]:


model.summary()


# In[15]:


# Visualize the model metrics in TensorBoard.
#docs_infra: no_execute
get_ipython().run_line_magic('load_ext', 'tensorboard')
get_ipython().run_line_magic('tensorboard', '--logdir logs')


# # Retrieve the trained word embeddings and save them to disk

# In[16]:


# Next, retrieve the word embeddings learned during training. The embeddings are weights of the Embedding layer in the model. 
# The weights matrix is of shape (vocab_size, embedding_dimension).
weights = model.get_layer('embedding').get_weights()[0]
vocab = vectorize_layer.get_vocabulary()


# In[17]:


# copying the vectors and metadata to files to use them to visualize word embeddings
out_v = io.open('vectors.tsv', 'w', encoding='utf-8')
out_m = io.open('metadata.tsv', 'w', encoding='utf-8')

for index, word in enumerate(vocab):
  if index == 0:
    continue  # skip 0, it's padding.
  vec = weights[index]
  if word is not None and word !=' ' and word != '\t' and (not word.startswith(' ') )and (not word.startswith('\t')):
    out_v.write('\t'.join([str(x) for x in vec]) + "\n")
    out_m.write(word + "\n")
out_v.close()
out_m.close()


# these files will be then use in comparer.ipynb

