/bin/rm -f fslvbm2a.sh
for g in `$FSLDIR/bin/imglob *_struc.*` ; do
    echo "echo ${g}; $FSLDIR/bin/fast -R 0.3 -H 0.1 ${g}_brain ; \
          $FSLDIR/bin/immv ${g}_brain_pve_1 ${g}_GM" >> fslvbm2a.sh
done
chmod a+x fslvbm2a.sh
