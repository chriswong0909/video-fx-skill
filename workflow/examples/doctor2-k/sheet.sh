source ~/hf/env.sh; export HYPERFRAMES_SKIP_SKILLS=1; cd ~/hf/d2k; rm -rf snapshots
timeout 170 npx hyperframes snapshot --at "$1" --no-end --describe false --timeout 15000 . >/dev/null 2>&1
O="$HOME/mnt/Video editing/doctor2/_work/d2k"; python3 -c "
from PIL import Image, ImageDraw
import glob
fs=sorted(glob.glob('snapshots/frame-*.png'))
W,H=360,640;cols=7;rows=(len(fs)+6)//7
sh=Image.new('RGB',(W*cols,H*rows),(40,40,40))
for i,f in enumerate(fs):
  im=Image.open(f).convert('RGB').resize((W,H)); sh.paste(im,((i%cols)*W,(i//cols)*H)); ImageDraw.Draw(sh).text(((i%cols)*W+6,(i//cols)*H+6),f.split('-at-')[1][:-4],fill=(255,0,0))
sh.save('$O/$2',quality=82)"; ls snapshots | wc -l
