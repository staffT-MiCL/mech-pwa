# キャラクターイラストの処理（重装操機）
# 使い方:
#   python3 char_portrait.py key 元画像.jpg 名前        … グリーンバックを透過 → 名前_raw.png
#   python3 char_portrait.py fit 名前_raw.png 出力.png 顔の中心x あごy
#        … 頭のてっぺん〜あごの長さ 300px・頭のてっぺん y=60 にそろえ、600×803 の透過PNGに（座標は元画像のピクセル）
#   python3 char_portrait.py small 出力.png            … 256色に減色して軽くする（pip install imagequant）
import sys
from PIL import Image
import numpy as np
W,H,TOP,HH=600,803,60,300
def key(src,name):
    im=np.array(Image.open(src).convert('RGB')).astype(float);r,g,b=im[...,0],im[...,1],im[...,2]
    d=g-np.maximum(r,b);a=np.clip(1-(d-40)/80,0,1);g2=np.where(d>0,np.maximum(r,b),g)
    Image.fromarray(np.dstack([r,g2,b,a*255]).astype(np.uint8)).save(name+'_raw.png')
def fit(raw,out,cx,chin):
    im=Image.open(raw);a=np.array(im)[...,3];top=int(np.argmax((a[:,cx-60:cx+60]>128).any(1)))
    s=HH/(chin-top);im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    ox,oy=round(W/2-cx*s),round(TOP-top*s);arr=np.array(im);bot=oy+arr.shape[0]
    if bot<H:arr=np.vstack([arr,np.repeat(arr[-1:],H-bot,0)])
    im=Image.fromarray(arr);c=Image.new('RGBA',(W,H),(0,0,0,0));c.paste(im,(ox,oy),im);c.save(out)
def small(p):
    import imagequant
    imagequant.quantize_pil_image(Image.open(p).convert('RGBA'),dithering_level=1.0,max_quality=95,min_quality=70).save(p,optimize=True)
c=sys.argv[1]
if c=='key':key(sys.argv[2],sys.argv[3])
elif c=='fit':fit(sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]))
elif c=='small':small(sys.argv[2])
