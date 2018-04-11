/bin/rm -f fslvbm3b.sh
for g in `$FSLDIR/bin/imglob *_struc.*` ; do
  #for j in 2 3 4 ; do
  for j in 3 ; do
    echo "echo ${g}; ${FSLDIR}/bin/fslmaths ${g}_GM_to_template_GM_mod -s ${j} ${g}_GM_to_template_GM_mod_s${j}" >> fslvbm3b.sh
  done
done
chmod a+x fslvbm3b.sh
