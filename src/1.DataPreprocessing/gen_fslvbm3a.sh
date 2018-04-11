/bin/rm -f fslvbm3a.sh
for g in `$FSLDIR/bin/imglob *_struc.*` ; do
  echo "echo ${g}; Rscript x_brain_registration_fslvbm3a.R ${g}_GM.nii.gz ${g}_GM_to_template_GM; \
        $FSLDIR/bin/fslmaths ${g}_GM_to_template_GM -mul ${g}_GM_to_template_GM_JAC_nl ${g}_GM_to_template_GM_mod -odt float" >> fslvbm3a.sh
done
chmod a+x fslvbm3a.sh
