#!/usr/bin/env python3
"""RVM 人像退地：python3 tools/matte.py in.mp4 out.webm [downsample=0.25]
輸出 VP9 帶 alpha webm（可直接放入 HyperFrames <video>）。
需要：pip install onnxruntime numpy；模型（約 15MB）第一次自動下載去 ~/.cache/rvm/。
速度：2 核 CPU 大約 3.3 幀／秒（20 秒片約 3 分鐘）。"""
import sys, subprocess, json, os, urllib.request, numpy as np, onnxruntime as ort
src, dst = sys.argv[1], sys.argv[2]
ds = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
M = os.path.expanduser('~/.cache/rvm/rvm_mobilenetv3_fp32.onnx')
if not os.path.exists(M):
    os.makedirs(os.path.dirname(M), exist_ok=True)
    urllib.request.urlretrieve('https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx', M)
pr = json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
     '-show_entries','stream=width,height,r_frame_rate','-of','json',src]))['streams'][0]
W, H, fps = pr['width'], pr['height'], pr['r_frame_rate']
sess = ort.InferenceSession(M, providers=['CPUExecutionProvider'])
rd = subprocess.Popen(['ffmpeg','-v','error','-i',src,'-f','rawvideo','-pix_fmt','rgb24','-'], stdout=subprocess.PIPE)
wr = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',fps,'-i','-',
     '-c:v','libvpx-vp9','-pix_fmt','yuva420p','-b:v','6M','-deadline','realtime','-cpu-used','8','-auto-alt-ref','0',dst], stdin=subprocess.PIPE)
rec = [np.zeros([1,1,1,1], np.float32)]*4
dr = np.array([ds], np.float32); n = 0
while True:
    b = rd.stdout.read(W*H*3)
    if len(b) < W*H*3: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    x = (f.astype(np.float32)/255).transpose(2,0,1)[None]
    fgr, pha, *rec = sess.run(None, {'src':x,'r1i':rec[0],'r2i':rec[1],'r3i':rec[2],'r4i':rec[3],'downsample_ratio':dr})
    a = (np.clip(pha[0,0],0,1)*255).astype(np.uint8)
    wr.stdin.write(np.dstack([f, a]).tobytes()); n += 1
    if n % 60 == 0: print(n, flush=True)
wr.stdin.close(); wr.wait(); print('done', n)
