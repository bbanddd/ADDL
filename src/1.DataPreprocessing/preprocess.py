#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import argparse
import subprocess


parser = argparse.ArgumentParser(description='Preprocess Pipeline.')
parser.add_argument('inputDir',
                    help='Directory containing data to preprocess')
parser.add_argument('--scriptsDir', default='./',
                    help='Directory where preprocess scripts locate, relative to working directory')
args = parser.parse_args()

inputDir = args.inputDir
scriptsDir = args.scriptsDir
if inputDir[-1] != '/'  : inputDir += '/'
if scriptsDir[-1] != '/': scriptsDir += '/'

scriptList = [
  "fslvbm1a.sh", 
  "gen_fslvbm1b.sh",
  "fslvbm1c.sh", 
  "gen_fslvbm2a.sh",
  "gen_fslvbm2b.sh",
  "gen_fslvbm2c.sh",
  "gen_fslvbm2d.sh",
  "gen_fslvbm2e.sh",
  "gen_fslvbm3a.sh",
  "gen_fslvbm3b.sh",
  "x_brain_extraction.R",
  "x_brain_registration.R",
  "x_brain_registration_fslvbm3a.R"
]

def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd )
  ret = subprocess.call(cmd, shell=True)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)


for item in scriptList:
  if not os.path.exists(scriptsDir + item):
    print('ERROR: script not exist', item)
    sys.exit(-1)


##### fslvbm1a
prevDir = os.getcwd()
exec_cmd('cp ' + scriptsDir + scriptList[0] + ' ' + inputDir)

os.chdir(inputDir)
exec_cmd('sh ' + scriptList[0])
os.chdir(prevDir)

assert os.path.exists(inputDir + 'struc/')
for item in scriptList[1:]:
  exec_cmd('cp ' + scriptsDir + item + ' ' + inputDir + 'struc/')


os.chdir(inputDir + 'struc/')

##### fslvbm1b
print('\n' + '='*20 + ' Brain Extraction ' + '='*20)
exec_cmd('sh ' + scriptList[1])
assert os.path.exists('./fslvbm1b.sh')
exec_cmd('./fslvbm1b.sh')

##### fslvbm1c
exec_cmd('sh ' + scriptList[2])

##### fslvbm2a
print('\n' + '='*20 + ' Grey Matter Extraction ' + '='*20)
exec_cmd('sh ' + scriptList[3])
assert os.path.exists('./fslvbm2a.sh')
exec_cmd('./fslvbm2a.sh')

##### fslvbm2b
print('\n' + '='*20 + ' Register to Standard Grey Matter Template ' + '='*20)
exec_cmd('sh ' + scriptList[4])
assert os.path.exists('./fslvbm2b.sh')
exec_cmd('./fslvbm2b.sh')

##### fslvbm2c
print('\n' + '='*20 + ' Generate Affine Study-Specific Template ' + '='*20)
exec_cmd('sh ' + scriptList[5])
assert os.path.exists('./fslvbm2c.sh')
exec_cmd('./fslvbm2c.sh')

##### fslvbm2d
print('\n' + '='*20 + ' Register to Affine Study-Specific Template ' + '='*20)
exec_cmd('sh ' + scriptList[6])
assert os.path.exists('./fslvbm2d.sh')
exec_cmd('./fslvbm2d.sh')

##### fslvbm2e
print('\n' + '='*20 + ' Generate Non-linear Study-Specific Template ' + '='*20)
exec_cmd('sh ' + scriptList[7])
assert os.path.exists('./fslvbm2e.sh')
exec_cmd('./fslvbm2e.sh')

##### fslvbm3a
print('\n' + '='*20 + ' Register to Non-linear Study-Specific Template and Modulate ' + '='*20)
exec_cmd('sh ' + scriptList[8])
assert os.path.exists('./fslvbm3a.sh')
exec_cmd('./fslvbm3a.sh')

##### fslvbm3b
print('\n' + '='*20 + ' Spatial Smoothing ' + '='*20)
exec_cmd('sh ' + scriptList[9])
assert os.path.exists('./fslvbm3b.sh')
exec_cmd('./fslvbm3b.sh')


exit(0)

