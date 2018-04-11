#!/usr/bin/env python

##### Generate labels based on filtered ADNIMERGE.csv
##    Label is organized as a dictionary,
##      Key  : PTID
##      Value: DX info, 0 for NL and 1 for AD

from __future__ import print_function


import pickle
import argparse
from common import adniMergeCsvColumnIndex

parser = argparse.ArgumentParser(description='Sort ADNIMERGE.csv by PTID')
parser.add_argument('inputFile',
                    help='Path to filtered ADNIMERGE.csv')
parser.add_argument('outputFile',
                    help='Path to output label file')
args = parser.parse_args()


inputFile  = args.inputFile
outputFile = args.outputFile



adniMergeCsvColumnIndex = {
'PTID'      : 0,
'VISCODE'   : 1,
'AGE'       : 2,
'PTGENDER'  : 3,
'CDRSB'     : 4,
'ADAS11'    : 5,
'MMSE'      : 6,
'DX'        : 7,
'FLDSTRENG' : 8,
'COLPROT'   : 9,
'ORIGPROT'  : 10,
'APOE4'     : 11,
'FDG'       : 12
}


# NL: 0, AD: 1, MCI: 2
def str2label(instr):
  if instr == 'NL':
    retval = 0 
  elif instr == 'AD':
    retval = 1 
  else:
    print('ERROR: impossible value ', instr)
    exit(-1)

  return retval


labels = {}
with open(inputFile, 'r') as ifile:
  for line in ifile:
    splitRes = str.split(line, ',')
    k = splitRes[adniMergeCsvColumnIndex['PTID']]
    v = str2label(splitRes[adniMergeCsvColumnIndex['DX']])

    if not k in labels:
      labels[k] = v
    else:
      if v != labels[k]:
        print('ERROR: subject diagnosis info mismatch')


cnt_lab = [0, 0]
for kk in labels:
  cnt_lab[labels[kk]] += 1
  

print('Number of labels: ', len(labels))
print(cnt_lab)


with open(outputFile, 'wb') as ofile:
  pickle.dump(labels, ofile)

