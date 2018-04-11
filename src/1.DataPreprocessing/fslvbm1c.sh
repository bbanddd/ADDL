imagelist=""
for g in `$FSLDIR/bin/imglob *_struc.*` ; do
  imagelist="$imagelist $g ${g}_brain"
done
$FSLDIR/bin/slicesdir -o $imagelist
