BINOUT="fslvbm1b.sh"

rm -f ${BINOUT}
for g in `$FSLDIR/bin/imglob *_struc.*` ; do
  echo "echo ${g}; Rscript x_brain_extraction.R ${g}.nii ${g}_brain" >> ${BINOUT}
done
chmod +x ${BINOUT}

