import os
import re
import numpy as np
import pickle
from tflearn.data_utils import shuffle


def load_batch(fpath):
  with open(fpath, 'rb') as infile:
    data_loaded = pickle.load(infile)
  data   = data_loaded['data']
  labels = data_loaded['labels']

  return data, labels

# dtype: train | test
def load_data_internal(dirname, dtype):
  print ''

  all_data   = []
  all_labels = []

  if dtype != 'train' and dtype != 'test':
    print 'ERROR: data type can only be train | test, got', dtype
    exit(-1)

  data_files = []
  for root,dirs,files in os.walk(dirname):
    if files:
      for ff in files:
        if dtype == 'train':
          if re.search(r'train_MRI', ff) != None:
            data_files.append( os.path.join(root, ff) )
        else:
          if re.search(r'test_MRI', ff) != None:
            data_files.append( os.path.join(root, ff) )

  is_first_file = True
  for item in data_files:
    print 'Reading ', item
    data, labels = load_batch(item)
    if is_first_file:
      all_data   = data
      all_labels = labels
      is_first_file = False
    else:
      all_data   = np.concatenate((all_data  , data  ), axis=0)
      all_labels = np.concatenate((all_labels, labels), axis=0)

  if len(all_data) != len(all_labels):
    print 'ERROR: data and label length mismatch, exit.'
    exit(-1)
  print 'Done read. Total number of elements: ', len(all_data)

  all_data = all_data / 255.0

  # shuffle before return
  all_data, all_labels = shuffle(all_data, all_labels)

  print 'Number of data [%s]: %d' %( dtype, len(all_data) )
  print ''

  return all_data, all_labels


def load_data(dirname, holder=''):
  X_train, Y_train = load_data_internal(dirname, 'train')
  X_test , Y_test  = load_data_internal(dirname, 'test' )
  return (X_train, Y_train), (X_test, Y_test)

#(X_T, Y_T), (X_TE, Y_TE) = load_data('../03.png2pickle/data_pkl_allMRI_32x32x1', 'MRI')


def load_test_sbj(pklfile):
  data = []
  labels = []

  with open(pklfile, 'rb') as infile:
    data_sbj = pickle.load(infile)

  data = data_sbj['data']
  labl = data_sbj['label']

  is_first_lab = True
  for ii in xrange(len(data)):
    if is_first_lab:
      labels = np.array([labl])
      is_first_lab = False
    else:
      labels = np.concatenate((labels, np.array([labl])), axis=0)

  assert len(labels) == len(data)

  return data, labels

def load_test_data_sbj(dirname):
  all_data = []
  all_labels = []

  data_files = []
  for root,dirs,files in os.walk(dirname):
    if files:
      for ff in files:
        if re.search(r'.pkl', ff) != None:
          data_files.append(os.path.join(root,ff))

  is_first_sbj = True
  for item in data_files:
    data, label = load_test_sbj(item)
    if is_first_sbj:
      all_data = data
      all_labels = label
      is_first_sbj = False
    else:
      all_data = np.concatenate((all_data, data), axis=0)
      all_labels = np.concatenate((all_labels, label), axis=0)

  all_data = all_data / 255.0

  print 'Total pkl files :', len(data_files)
  print 'all_data.shape  :', all_data.shape
  print 'all_labels.shape:', all_labels.shape

  return all_data, all_labels

