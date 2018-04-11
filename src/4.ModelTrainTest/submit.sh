#!/bin/bash

if [ $# -ne 1 ]; then
  echo "ERROR: wrong number of arguments given."
  echo "Usage: `basename $0` <script>"
  exit -1
fi

LOG_DIR="log"

[ ! -e $LOG_DIR ] && mkdir $LOG_DIR

scriptName=$1
logFile=$LOG_DIR/${scriptName}.log
JOB="python $scriptName > $logFile 2>&1"

$JOB > $logFile 2>&1 &

exit 0

