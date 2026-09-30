#!/bin/bash
# uso: render.sh work.pptx outdir p1 p2 ...
. /tmp/env.sh
f=$1; out=$2; shift 2
mkdir -p $out; rm -f $out/*.png
python3 $S/office/soffice.py --headless --convert-to pdf --outdir $out $f >/dev/null 2>&1
python3 - "$out" "$@" <<'PY'
import sys, pymupdf, glob
out=sys.argv[1]; pdf=glob.glob(out+'/*.pdf')[0]
d=pymupdf.open(pdf)
for n in map(int,sys.argv[2:]):
    d[n-1].get_pixmap(dpi=80).save(f'{out}/s{n:03d}.png')
print(len(d),'pages')
PY
