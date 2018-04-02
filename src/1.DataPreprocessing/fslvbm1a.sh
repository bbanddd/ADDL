#!/bin/sh

mkdir -p struc
for g in `$FSLDIR/bin/imglob *` ; do
  echo $g
  imcp $g struc/${g}_struc
done

