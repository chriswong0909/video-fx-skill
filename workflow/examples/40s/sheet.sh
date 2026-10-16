#!/bin/bash
# sheet.sh 時間,時間 輸出.jpg ：逐拍截圖砌 contact sheet（自己先睇）
export HYPERFRAMES_SKIP_SKILLS=1; cd "$(dirname "$0")"; rm -rf snapshots
npx hyperframes snapshot --at "$1" --no-end --describe false --timeout 15000 . > snap.log 2>&1
python3 -c "
from PIL import Image, ImageDraw
import glob,sys
fs=sorted(glob.glob('snapshots/*.png'), key=lambda f: float(f.split('-at-')[1][:-5].replace('s','')) if '-at-' in f else 0)
W,H=360,640;cols=min(6,len(fs));rows=(len(fs)+cols-1)//cols
sh=Image.new('RGB',(W*cols,H*rows),(40,40,40))
for i,f in enumerate(fs):
  im=Image.open(f).convert('RGB').resize((W,H)); sh.paste(im,((i%cols)*W,(i//cols)*H)); ImageDraw.Draw(sh).text(((i%cols)*W+6,(i//cols)*H+6),f.split('/')[-1][:-4],fill=(255,0,0))
sh.save('$2',quality=85)"; ls snapshots | wc -l; tail -3 snap.log
