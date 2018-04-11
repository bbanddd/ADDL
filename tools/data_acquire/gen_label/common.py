
from __future__ import print_function

import subprocess


adniMergeCsvTempDir = '/tmp/ADNIMERGE_csv/'

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
  'FDG'       : 12,
  'EXAMDATE'  : 13
}


## Description:
##   Execute command @cmd and verify command return status, exit if fail
##
## Parameters:
##   @cmd: command to execute
##
## Return value:
##   None
##
def exec_cmd(cmd):
  print('exec_cmd(): cmd = ', cmd )
  ret = subprocess.call(cmd, shell=True)
  if ret != 0:
    print('!!!FAILED!!!, exit.')
    exit(-1)


if __name__ == '__main__':
  exec_cmd('ls -l')

