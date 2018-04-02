#!/usr/bin/env python

from __future__ import print_function

import os
import re
import argparse
import pickle

parser = argparse.ArgumentParser(description='Reorganize MRI PNG files by class, NL|MCI|AD')
parser.add_argument('inputDir',
                    help='Input directory containing decomposed png files')
parser.add_argument('outputDir',
                    help='Output directory to contain organized png files by class')
parser.add_argument('labelFile',
                    help='Label file')
args = parser.parse_args()

inputDir  = args.inputDir
labelFile = args.labelFile
outputDir = args.outputDir
if inputDir[-1] != '/' : inputDir  += '/'
if outputDir[-1] != '/': outputDir += '/'

labels = {}
cnt_NL  = 0
cnt_MCI = 0
cnt_AD  = 0

subject_no_label = []


def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd)
  ret = os.system(cmd)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)


def get_class(item):
  global cnt_NL
  global cnt_MCI
  global cnt_AD

  global subject_no_label

  k = item[5:15]
  if not k in labels:
    print('ERROR: label not found,', k)
    subject_no_label.append(k)
    return None

  label = labels[k]
  retval = ''
  if label == 0:
    retval = 'NL'
    cnt_NL = cnt_NL + 1
  elif label == 1:
    retval = 'AD'
    cnt_AD = cnt_AD + 1
  elif label == 2:
    retval = 'MCI'
    cnt_MCI = cnt_MCI + 1
  else:
    print('ERROR: impossible value ', label)
    exit(-1)

  return retval


def reorganize(item):
  dir_class = get_class(item)
  if None == dir_class:
    return

  l_out_dir = outputDir + dir_class
  if not os.path.exists(l_out_dir):
    exec_cmd('mkdir ' + l_out_dir)

  cmd = 'cp -r ' + inputDir + '/' + item + ' ' + l_out_dir
  exec_cmd(cmd)


if not os.path.exists(labelFile):
  print('ERROR: labels file not exist, exit.')
  exit(-1)

with open(labelFile, 'rb') as ifile:
  labels = pickle.load(ifile)
print('Total number of labels: ', len(labels))

if not os.path.exists(outputDir):
  exec_cmd('mkdir ' + outputDir)

input_files = []
for root,dirs,files in os.walk(inputDir):
  if dirs:
    for item in dirs:
      if re.search(r'ADNI_', item) != None:
        input_files.append(item)
print(len(input_files))

for item in input_files:
  reorganize(item)

print('NL : ', cnt_NL)
print('AD : ', cnt_AD)
print('MCI: ', cnt_MCI)

print('Number of subjects not in dictionary:', len(subject_no_label))
for item in subject_no_label:
  print(item)

exit(0)

