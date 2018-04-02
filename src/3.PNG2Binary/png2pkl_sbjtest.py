#!/usr/bin/env python

from __future__ import print_function

import os
import re
import argparse
import cv2 
import numpy as np
import pickle
import random


parser = argparse.ArgumentParser(description='Load PNGs, turn into 4D matrices for each subject and store using pickle')
parser.add_argument('inputDir',
                    help='Input directory containing testing set png files')
parser.add_argument('outputDir',
                    help='Output directory to contain binary data')
parser.add_argument('--labelFile',
                    help='Label file')
args = parser.parse_args()

inputDir  = args.inputDir
outputDir = args.outputDir
labelFile = args.labelFile
if inputDir[-1] != '/' : inputDir  += '/'
if outputDir[-1] != '/': outputDir += '/'

if labelFile != None:
  has_label = True
else:
  has_label = False

labels = {}


def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd)
  ret = os.system(cmd)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)


def get_id_label(subject):
  res = str.split(subject, '/')
  sbj_id = res[-1]

  if has_label:
    k = sbj_id[5:15]
    if not k in labels:
      print('ERROR: label not found,', k)
      exit(-1)

    sbj_lab = labels[k]
    assert (0 == sbj_lab) or (1 == sbj_lab)
  else:
    sbj_lab = None

  return sbj_id, sbj_lab


def process(subject):
  print(subject)

  subject_id, subject_lab = get_id_label(subject)

  all_pngs = []
  for root,dirs,files in os.walk(subject):
    if files:
      all_pngs = files
  all_pngs.sort()

  data_png = []
  is_first_file = True
  for item in all_pngs:
    fpng = cv2.imread(subject+'/'+item, cv2.IMREAD_GRAYSCALE)
    fpng = cv2.resize(fpng, (32,32))
    fpng = fpng.reshape(fpng.shape[0], fpng.shape[1], 1)

    if is_first_file:
      data_png = np.array([fpng])
      is_first_file = False
    else:
      data_png = np.concatenate((data_png, np.array([fpng])), axis=0)

  if has_label:
    subject_data = { 'id': subject_id, 'label': subject_lab, 'data': data_png }
    print(subject_data['id'], subject_data['label'], subject_data['data'].shape)
  else:
    subject_data = { 'id': subject_id, 'data': data_png }
    print(subject_data['id'], subject_data['data'].shape)

  return subject_data


def data2pkl(sbjdata, subject):
  lab_list = ['NL', 'AD']
  res = str.split(subject, '/')
  if has_label:
    exp_label = res[-2]
    assert exp_label == lab_list[sbjdata['label']]
  else:
    exp_label = 'NoLabel'

  outdir = outputDir + exp_label
  exec_cmd('mkdir -p ' + outdir)
  with open(outdir+'/'+exp_label+'_'+sbjdata['id']+'.pkl', 'wb') as ofile:
    pickle.dump(sbjdata, ofile)


if has_label and not os.path.exists(labelFile):
  print('ERROR: labels file not exist, exit.')
  exit(-1)

if has_label:
  with open(labelFile, 'rb') as ifile:
    labels = pickle.load(ifile)
  print('Number of labels: ', len(labels))

if not os.path.exists(outputDir):
  exec_cmd('mkdir ' + outputDir)

input_subject_dirs = []
for root,dirs,files in os.walk(inputDir):
  if dirs and (re.search(r'ADNI_', dirs[0]) != None):
    for item in dirs:
      input_subject_dirs.append(os.path.join(root, item))

for item in input_subject_dirs:
  print('')
  sbjdata = process(item)
  data2pkl(sbjdata, item)


print('Done. Total number of subjects: ', len(input_subject_dirs))

