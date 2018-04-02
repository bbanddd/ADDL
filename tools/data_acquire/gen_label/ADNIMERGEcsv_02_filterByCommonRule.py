#!/usr/bin/env python

##### Filter ADNIMERGE.csv without quotation and sorted


from __future__ import print_function

import os
import sys
import csv
import pprint
import argparse
from common import exec_cmd, adniMergeCsvTempDir, adniMergeCsvColumnIndex


parser = argparse.ArgumentParser(description='Filter ADNIMERGE.csv without quotation and sorted')
parser.add_argument('inputFile',
                    help = 'Path to ADNIMERGE.csv without quotation and sorted')
parser.add_argument('outputFile',
                    help = 'Path to filtered file')
args = parser.parse_args()


inputFile  = args.inputFile
outputFile = args.outputFile

stage1ofile = adniMergeCsvTempDir + 'stage1_ADNIMERGE_coi.csv'
stage2ofile = adniMergeCsvTempDir + 'stage2_ADNIMERGE_UNIFORM_DX.csv'
stage3ofile = adniMergeCsvTempDir + 'stage3_ADNIMERGE_UNIFORM_DX_AD_NL.csv'
stage3ofile_vid    = adniMergeCsvTempDir + 'stage3_ADNIMERGE_UNIFORM_DX_AD_NL_sortByVID.csv'
stage3ofile_vid_dx = adniMergeCsvTempDir + 'stage3_ADNIMERGE_UNIFORM_DX_AD_NL_sortByVID_withDX.csv'


cntRecord = {
'TOTAL' : 0,
'DX'    : 0,
'EDX'   : 0
}

dxBySubject = {}

cntClass = {
'NL'  : 0,
'AD'  : 0,
'MCI' : 0,
''    : 0
}

uniformDXSubject = []


##### Functions definition


## Description: 
##   Fill dictionary dxBySubject.
##   Key  : PTID
##   Value: list of diagnosis information of every visit
##   
## Parameters:
##   @ifilename: CSV file containing patient records
##
## Return value:
##   None
##
def fillDXbySubject(ifilename):
  global dxBySubject
  dxBySubject = {}

  with open(ifilename, 'r') as ifile:
    for line in ifile:
      splitRes = str.split(line, ',')
      k = splitRes[adniMergeCsvColumnIndex['PTID']]
      v = splitRes[adniMergeCsvColumnIndex['DX']]
      dxBySubject.setdefault(k,[]).append(v)


## Description:
##   Pick up all records of patient in list uniformDXSubject 
##   from @ifilename and store in @ofilename
##
## Parameters:
##   @ifilename: CSV file containing patient records
##   @ofilename: output filename
##
## Return value:
##   None
##
def pickUpUniformDX(ifilename, ofilename):
  ofile = open(ofilename, 'w')

  with open(ifilename, 'r') as ifile:
    for line in ifile:
      splitRes = str.split(line, ',')
      if splitRes[adniMergeCsvColumnIndex['PTID']] in uniformDXSubject:
        ofile.write(line)

  ofile.close()


## Description:
##   Print statistics information of current filter stage. Information include,
##   1) Total number of subjects/patients
##   2) Number of subject/patient in each class
##   3) Number of NIfTI file in each class
##
## Parameters:
##   @ifilename: CSV file containing patient records
##
## Return value:
##   None
##
def printSubjectRecordInfo(ifilename):
  cntRecordClass  = {'NL' : 0, 'AD' : 0, 'MCI' : 0, '' : 0}
  cntSubjectClass = {'NL' : 0, 'AD' : 0, 'MCI' : 0}

  fillDXbySubject(ifilename)

  for k in dxBySubject:
    v = dxBySubject[k]

    for item in v:
      cntRecordClass[item] += 1

    for item in v:
      if item != '': 
        cntSubjectClass[item] += 1
        break

  print('Number of subjects:', len(dxBySubject))
  print('Subject DX distribution    :', cntSubjectClass)
  print('NIfTI file DX distribution :', cntRecordClass)



##### Main Start

if not os.path.exists(inputFile):
  print('ERROR: inputFile not exists,',inputFile)
  sys.exit(-1)


##### Select columns of interest
cmd = "awk -F ',' '{OFS=\",\"} {print $2,$3,$9,$10,$19,$20,$22,$52,$43,$5,$6,$15,$16,$7}' " + inputFile + " > " + stage1ofile;exec_cmd(cmd)
cmd = "sed -i 's/\"//g' " + stage1ofile;          exec_cmd(cmd)
cmd = "sed -i 's/Dementia/AD/g' " + stage1ofile;  exec_cmd(cmd)
cmd = "sed -i 's/CN/NL/g' " + stage1ofile;        exec_cmd(cmd)
fillDXbySubject(stage1ofile)

print('Number of subjects:', len(dxBySubject))
for k in dxBySubject:
  v = dxBySubject[k]
  for item in v:
    cntClass[item] += 1

  ##### Get rid of subjects with all empty DX, and subjects with more than one valid DX
  ##    Keep subjects with only one valid DX and with or without empty DX
  vSet = set(v)
  if (len(vSet) == 1) and (not '' in vSet):
    uniformDXSubject.append(k)
  elif (len(vSet) == 2) and ('' in vSet):
    uniformDXSubject.append(k)
  else:
    pass

print('NIfTI file DX distribution:', cntClass)
print('Number of subject with uniform DX:', len(uniformDXSubject))


##### Pickup subjects with uniform DX
pickUpUniformDX(stage1ofile, stage2ofile)
print('='*10 + ' after pickUpUniformDX() ' + '='*10)
printSubjectRecordInfo(stage2ofile)


##### Remove MCI records
ADNLSubject = []
fillDXbySubject(stage2ofile)
for k in dxBySubject:
  v = dxBySubject[k]
  if not 'MCI' in v:
    ADNLSubject.append(k)

ofile = open(stage3ofile, 'w')
with open(stage2ofile, 'r') as ifile:
  for line in ifile:
    splitRes = str.split(line, ',')
    if splitRes[adniMergeCsvColumnIndex['PTID']] in ADNLSubject:
      ofile.write(line)
ofile.close()

print('='*10 + ' after filter out MCI ' + '='*10)
printSubjectRecordInfo(stage3ofile)


##### The following code is to filter records based on cognition test scores

'''

##### Filter data by score range
scoresNL = {'CDRSB': [-0.096, 0.156], 'ADAS11': [2.800 ,  8.800], 'MMSE': [27.900, 30.300]}
scoresAD = {'CDRSB': [ 2.811, 6.203], 'ADAS11': [13.700, 27.900], 'MMSE': [21.000, 25.200]}

stage4ofile = 'stage4_ADNIMERGE_UNIFORM_DX_AD_NL_sortByVID_withDX_NEDX_FILTER_SCORE.csv'

ofile = open(stage4ofile, 'w')
with open('stage3_ADNIMERGE_UNIFORM_DX_AD_NL_sortByVID_withDX_NEDX.csv', 'r') as ifile:
  for line in ifile:
    splitRes = str.split(line, ',')
    DX = splitRes[adniMergeCsvColumnIndex['DX']]
  
    if splitRes[adniMergeCsvColumnIndex['CDRSB']] == '':
      if DX == 'NL': CDRSB = scoresNL['CDRSB'][0]
      elif DX == 'AD': CDRSB = scoresAD['CDRSB'][1]
      else: exit(0)
    else:
      CDRSB = float(splitRes[adniMergeCsvColumnIndex['CDRSB']])

    if splitRes[adniMergeCsvColumnIndex['ADAS11']] == '':
      if DX == 'NL': ADAS11 = scoresNL['ADAS11'][0]
      elif DX == 'AD': ADAS11 = scoresAD['ADAS11'][1]
      else: exit(0)
    else:
      ADAS11 = float(splitRes[adniMergeCsvColumnIndex['ADAS11']])

    if splitRes[adniMergeCsvColumnIndex['MMSE']] == '':
      if DX == 'NL': MMSE = scoresNL['MMSE'][1]
      elif DX == 'AD': MMSE = scoresAD['MMSE'][0]
      else: exit(0)
    else:
      MMSE = float(splitRes[adniMergeCsvColumnIndex['MMSE']])

    if (DX == 'NL') and (CDRSB < scoresNL['CDRSB'][1]) and (ADAS11 < scoresNL['ADAS11'][1]) and (MMSE > scoresNL['MMSE'][0]):
      ofile.write(line)
    elif (DX == 'AD') and (CDRSB > scoresAD['CDRSB'][0]) and (ADAS11 > scoresAD['ADAS11'][0]) and (MMSE < scoresAD['MMSE'][1]):
      ofile.write(line)
    else:
      pass
      #print(line[:-1])

ofile.close()

print('='*10 + ' after filter scores ' + '='*10)
printSubjectRecordInfo(stage4ofile)

'''


##### Sort by VISCODE

## Key  : PTID
## Value: list of patient records 
sbjDictPhase1 = {}

## Key  : PTID
## Value: dictionary 
##          key  : VISCODE mapped to integer
##          value: patient record of visit specified by key
sbjDictPhase2 = {}

with open(stage3ofile, 'r') as ifile:
  for line in ifile:
    splitRes = str.split(line, ',')
    k = splitRes[adniMergeCsvColumnIndex['PTID']]
    sbjDictPhase1.setdefault(k,[]).append(line)


for kk in sbjDictPhase1:
  vv = sbjDictPhase1[kk]

  sbjDict = {}
  for line in vv:
    splitRes = str.split(line, ',')
    k = splitRes[adniMergeCsvColumnIndex['VISCODE']]
    if k == 'bl':
      k = 0
    else:
      k = int(k[1:])
    assert not k in sbjDict
    sbjDict[k] = line

  assert not kk in sbjDictPhase2
  sbjDictPhase2[kk] = sbjDict

#pprint.pprint(sbjDictPhase2['002_S_0413'])


sbjDictPhase2Keys = sbjDictPhase2.keys()
sbjDictPhase2Keys.sort()
#pprint.pprint(sbjDictPhase2Keys)

ofile = open(stage3ofile_vid, 'w')
for kk in sbjDictPhase2Keys:
  vv = sbjDictPhase2[kk]
  vvKeys = vv.keys()
  vvKeys.sort()
  for k in vvKeys:
    ofile.write(vv[k])

ofile.close()


##### Infer empty DX
###   If DX of the first visit (VISITID = bl) is AD, all DX for subsequent visits are AD
###   If the last non-empty DX is NL, all DX before that are NL

sbjDictPhase1 = {}
sbjDictPhase2 = {}

with open(stage3ofile_vid, 'r') as ifile:
  for line in ifile:
    line = line[:-1]
    splitRes = str.split(line, ',')
    k = splitRes[adniMergeCsvColumnIndex['PTID']]
    sbjDictPhase1.setdefault(k,[]).append(splitRes)

#pprint.pprint(sbjDictPhase1['002_S_0413'])

for kk in sbjDictPhase1:
  vv = sbjDictPhase1[kk]
  # If first is AD, then all are AD
  if vv[0][adniMergeCsvColumnIndex['DX']] == 'AD':
    for item in vv:
      item[adniMergeCsvColumnIndex['DX']] = 'AD'
  else:
    lastNLIdx = len(vv)-1
    for item in vv[::-1]:
      if item[adniMergeCsvColumnIndex['DX']] == '': lastNLIdx -= 1
      else: break
    for item in vv[0:lastNLIdx]:
      item[adniMergeCsvColumnIndex['DX']] = 'NL'


ocsvfile = open(stage3ofile_vid_dx, 'wb')
owriter  = csv.writer(ocsvfile)
sbjDictPhase1Keys = sbjDictPhase1.keys()
sbjDictPhase1Keys.sort()
for kk in sbjDictPhase1Keys:
  vv = sbjDictPhase1[kk]
  for item in vv:
    owriter.writerow(item)
ocsvfile.close()


##### Remove EDX (Empty DX) records

ofile = open(outputFile, 'w')

cntEDX = 0
with open(stage3ofile_vid_dx, 'r') as ifile:
  for line in ifile:
    splitRes = str.split(line, ',')
    if splitRes[adniMergeCsvColumnIndex['DX']] == '':
      cntEDX += 1
    else:
      ofile.write(line)

print('Number of records with empty DX:', cntEDX)

ofile.close()


sys.exit(0)

