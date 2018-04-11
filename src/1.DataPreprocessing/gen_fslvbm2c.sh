cat <<stage_tpl3 > fslvbm2c.sh
#!/bin/sh
if [ -f ../template_list ] ; then
    template_list=\`cat ../template_list\`
    template_list=\`\$FSLDIR/bin/remove_ext \$template_list\`
else
    template_list=\`echo *_struc.* | sed 's/_struc\./\./g'\`
    template_list=\`\$FSLDIR/bin/remove_ext \$template_list | sort -u\`
    echo "WARNING - study-specific template will be created from ALL input data - may not be group-size matched!!!"
fi
for g in \$template_list ; do
    mergelist="\$mergelist \${g}_struc_GM_to_T"
done
\$FSLDIR/bin/fslmerge -t template_4D_GM \$mergelist
\$FSLDIR/bin/fslmaths template_4D_GM -Tmean template_GM
\$FSLDIR/bin/fslswapdim template_GM -x y z template_GM_flipped
\$FSLDIR/bin/fslmaths template_GM -add template_GM_flipped -div 2 template_GM_init
stage_tpl3
chmod +x fslvbm2c.sh

