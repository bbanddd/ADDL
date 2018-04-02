#!/usr/bin/env python

from __future__ import print_function

import os
import re
import argparse


parser = argparse.ArgumentParser(description='Pickup png files in each subject')
parser.add_argument('inputDir',
                    help='Input directory containing organized png files')
parser.add_argument('outputDir',
                    help='Output directory to contain selected png files')
parser.add_argument('pngLowIndex', type=int,
                    help='Png file index from which to select, include')
parser.add_argument('pngHighIndex', type=int,
                    help='Png file index till which to select, exclude')
args = parser.parse_args()


inputDir  = args.inputDir
outputDir = args.outputDir
pngLowIndex  = args.pngLowIndex
pngHighIndex = args.pngHighIndex
if inputDir[-1] != '/' : inputDir  += '/'
if outputDir[-1] != '/': outputDir += '/'


assert (pngLowIndex  >= 0) 
assert (pngHighIndex >= 0) 
assert (pngLowIndex  <= pngHighIndex)


def exec_cmd(cmd):
  #print('exec_cmd(): cmd = ', cmd)
  ret = os.system(cmd)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)

def strip(item):
  res = str.split(item, '/')

  startIdx = -1
  for ii in xrange(0, len(res)):
    if ('NL' == res[ii]) or ('AD' == res[ii]) or ('MCI' == res[ii]):
      startIdx = ii
      break

  internalOutDir = ''
  for iitem in res[startIdx:]:
    internalOutDir += iitem + '/'
  exec_cmd('mkdir -p ' + outputDir + internalOutDir)


  all_files = []
  for root,dirs,files in os.walk(item):
    if files:
      all_files = files
  all_files.sort()

  for kept_file in all_files[pngLowIndex:pngHighIndex]:
    cmd = 'cp ' + item + '/' + kept_file + ' ' + outputDir + internalOutDir
    exec_cmd(cmd)


if not os.path.exists(outputDir):
  exec_cmd('mkdir ' + outputDir)

input_files = []
for root,dirs,files in os.walk(inputDir):
  if dirs:
    for item in dirs:
      if re.search(r'ADNI_', item) != None:
        input_files.append(os.path.join(root, item))

for item in input_files:
  print(item)
  strip(item)

print(len(input_files))

