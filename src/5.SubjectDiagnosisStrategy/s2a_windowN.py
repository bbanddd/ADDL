#!/usr/bin/env python

from __future__ import print_function

import os
import csv
import sys

inputFile = sys.argv[1]

recordList = []

isFirstLine = True
with open(inputFile, 'r') as ifile:
  for line in ifile:
    if isFirstLine: isFirstLine = False; continue

    res = str.split(line[:-2], ',')
    assert len(res) == 69
    for ii in xrange(1, len(res)):
      res[ii] = int(res[ii])

    subjectRecord = []
    subjectRecord += res[:5]
    subjectRecord.append(res[7:])
    recordList.append(subjectRecord)

#print(recordList)
#print(len(recordList))


def windowN(N, sliceResList):
  assert N >= 1 and N <= 62

  cnt0 = 0
  cnt1 = 0

  for idx in xrange(0, len(sliceResList)-N+1):
    winList = sliceResList[idx:idx+N]

    '''
    if winList.count(1) > winList.count(0):
      cnt1 += 1
    else:
      cnt0 += 1
    '''

    if 0 in winList:
      cnt0 += 1
    else:
      cnt1 += 1

  if cnt0 >= cnt1:
    retval = 0
  else:
    retval = 1

  return retval


for N in xrange(1,63):
  totalSubject = 0
  totalRight   = 0

  for sbjRec in recordList:
    totalSubject += 1

    expRes = sbjRec[1]
    actRes = windowN(N, sbjRec[-1])
    if expRes == actRes: totalRight += 1
    #print(expRes, ',', actRes)

  #print('N:', N, 'totalSubject:', totalSubject, 'totalRight:', totalRight, 'Accuracy:', float(totalRight)/float(totalSubject))
  print(float(totalRight)/float(totalSubject))
