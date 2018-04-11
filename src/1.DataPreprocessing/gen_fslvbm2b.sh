T=${FSLDIR}/data/standard/tissuepriors/avg152T1_gray
/bin/rm -f fslvbm2b.sh
for g in `$FSLDIR/bin/imglob *_struc.*` ; do
  echo "echo ${g}; ${FSLDIR}/bin/fsl_reg ${g}_GM $T ${g}_GM_to_T -a" >> fslvbm2b.sh
done
chmod a+x fslvbm2b.sh
