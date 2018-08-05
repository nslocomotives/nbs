"""
open pre-trained glove word embedding
data from http://nlp.stanford.edu/projects/glove/
"""
# NOTE: to allow us to import modules from directory abouve we add it to the path with sysapend
import sys
sys.path.append("..")

import os
import numpy as np
import pickle
import get_config

dirs = get_config.cfg['dirs']

GLOVE_DIR = dirs['dataDir']
model_name = dirs['dataDir'] + 'glove_embeddings'

embeddings_index = {}
f = open(os.path.join(GLOVE_DIR, 'glove.42B.300d.txt'), encoding="utf8")
for line in f:
    values = line.split()
    word = values[0]
    coefs = np.asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

print('Found %s word vectors.' % len(embeddings_index))
print('Now writting the file to disk...')
modelFileSave = open(model_name, 'wb')
pickle.dump(embeddings_index, modelFileSave)
modelFileSave.close()
print('All Done :-)')
