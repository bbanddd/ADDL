#!/usr/bin/env python

from __future__ import print_function

import os
import re
import argparse
import cv2 
import numpy as np
import pickle
import random


parser = argparse.ArgumentParser(description='Store PNG files and labels in binary. \
1. Load png files, resize into 32x32 and store them in a 4D matrix; shape = (NunmerOfPNGFiles, 32, 32, 1) \
2. Load labels and store in a vector; shape = (NumberOfLabels, ) \
3. Organize PNG matrix and label vector in dictionary and store dictionary in binary file')

parser.add_argument('inputDir',
                    help='Input directory containing png files')

parser.add_argument('outputDir',
                    help='Output directory to contain pinary data')

parser.add_argument('labelFile',
                    help='Label file')

parser.add_argument('ofprefix',
                    help='Prefix of output filename, train_ | test_')

args = parser.parse_args()


inputDir  = args.inputDir
outputDir = args.outputDir
ofprefix  = args.ofprefix
labelFile = args.labelFile
if inputDir[-1] != '/' : inputDir  += '/'
if outputDir[-1] != '/': outputDir += '/'

assert (ofprefix == 'train_') or (ofprefix == 'test_')

outputModality = 'MRI'
labels = {}


def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd)
  ret = os.system(cmd)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)


def get_label(input_file):
  res = str.split(input_file, '/')
  if outputModality == 'MRI':
    k = res[-2][5:15]
  else:
    k = res[-3][5:15]
  if not k in labels:
    print('ERROR: label not found,', k)
    exit(-1)

  label = labels[k]
  assert (0 == label) or (1 == label)

  return label


def png2matrix(input_file):
  global is_first_file
  global data_png
  global label_png

  fpng = cv2.imread(input_file, cv2.IMREAD_GRAYSCALE)
  fpng = cv2.resize(fpng, (32,32))
  fpng = fpng.reshape(fpng.shape[0], fpng.shape[1], 1)

  if is_first_file:
    data_png  = np.array([fpng])

    label = get_label(input_file)
    label_png = np.array([label])

    is_first_file = False

  else:
    data_png = np.concatenate((data_png, np.array([fpng])), axis=0)

    label = get_label(input_file)
    label_png = np.concatenate((label_png, np.array([label])), axis=0)


def matrix2pkl(idx_pkl):
  global is_first_file
  global data_png
  global label_png

  if len(data_png) != len(label_png):
    print('ERROR: data and label length mismatch, exit.')
    exit(-1)

  print('Writing pkl: idx_pkl = %d, number of elements = %d, ' %(idx_pkl, len(data_png)), end='')
  print('data shape =', data_png.shape, ', label shape =', label_png.shape)

  dict_png = {'data': data_png, 'labels': label_png}
  with open(outputDir+ofprefix+outputModality+'_'+str(idx_pkl).zfill(4), 'wb') as ofile:
    pickle.dump(dict_png, ofile)

  data_png = []
  label_png = []
  is_first_file = True



if outputModality != 'MRI' and outputModality != 'fMRI':
  print('ERROR: outputModality can only be MRI | fMRI')
  exit(-1)

if not os.path.exists(labelFile):
  print('ERROR: labels file not exist, exit.')
  exit(-1)

with open(labelFile, 'rb') as ifile:
  labels = pickle.load(ifile)
print('Number of labels: ', len(labels))

if not os.path.exists(outputDir):
  exec_cmd('mkdir ' + outputDir)


input_files = []
for root,dirs,files in os.walk(inputDir):
  if files:
    for ff in files:
      if re.search(r'.png', ff) != None:
        input_files.append( os.path.join(root, ff) )


data_png = []
label_png = []
is_first_file = True

idx_file = 0
thresh_file = 10000
idx_pkl  = 0

for item in input_files:
  png2matrix(item)
  idx_file = idx_file + 1

  if ((idx_file % thresh_file) == 0) and (idx_file != 0):
    matrix2pkl(idx_pkl)
    idx_pkl = idx_pkl + 1

if len(data_png) != 0:
  matrix2pkl(idx_pkl)

print('Done. Total number of elements: ', idx_file)

