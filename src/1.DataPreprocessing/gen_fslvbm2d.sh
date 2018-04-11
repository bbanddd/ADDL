/bin/rm -f fslvbm2d.sh
for g in `$FSLDIR/bin/imglob *_struc.*` ; do
  echo "echo ${g}; Rscript x_brain_registration.R ${g}_GM.nii.gz ${g}_GM_to_T_init.nii.gz" >> fslvbm2d.sh
done
chmod a+x fslvbm2d.sh
