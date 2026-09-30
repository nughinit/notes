import sys
from PIL import Image
out=sys.argv[1]; files=sys.argv[2:]
ims=[Image.open(f) for f in files]
w,h=ims[0].size
cols=2; rows=(len(ims)+1)//2
sh=Image.new('RGB',(w*cols+10,h*rows+10*(rows-1)),'#888')
for i,im in enumerate(ims):
    sh.paste(im,((i%cols)*(w+10),(i//cols)*(h+10)))
sh.save(out)
