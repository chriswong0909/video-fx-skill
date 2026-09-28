# usage: python3 tools/relight.py SRC START_FRAME N_FRAMES OUT_PREFIX  (needs ~/rvm.onnx, see lessons/relight.md)
# usage: relight.py SRC START_FRAME N_FRAMES OUT_PREFIX [--warm K] [--debug]
import sys, subprocess, numpy as np, cv2, onnxruntime as ort, os, time
src, start, n, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
warm = 30
W, H, FPS = 1080, 1920, 30
so = ort.SessionOptions(); so.intra_op_num_threads = 4; so.log_severity_level = 3
sess = ort.InferenceSession(os.path.expanduser("~/rvm.onnx"), so, providers=["CPUExecutionProvider"])
rec = [np.zeros([1,1,1,1], np.float32)]*4
dsr = np.array([0.25], np.float32)
s0 = max(0, start - warm)
dec = subprocess.Popen(["ffmpeg","-v","error","-ss",f"{s0/FPS:.4f}","-i",src,"-frames:v",str(n+start-s0),
    "-f","rawvideo","-pix_fmt","rgb24","-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-c:v","libx264","-preset","medium","-crf","14","-pix_fmt","yuv420p", out+".mp4"], stdin=subprocess.PIPE)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
# key light: soft ellipse centred on face, offset camera-left/up (face ~ x .50, y .33)
fx, fy = 0.47*W, 0.30*H
key = np.exp(-(((xx-fx)/(0.30*W))**2 + ((yy-fy)/(0.20*H))**2))
# directional falloff left->right for modelling
side = np.clip(1.0 - (xx - 0.35*W)/(0.6*W), 0, 1)**1.2
key = (key * (0.6 + 0.4*side))[..., None]
vig = np.exp(-(((xx-0.5*W)/(0.75*W))**2 + ((yy-0.40*H)/(0.62*H))**2))[..., None]
def curve(x, lift, gain, gamma):
    return np.clip(lift + (1-lift)*np.power(np.clip(x,0,1), gamma)*gain, 0, 1)
t0=time.time(); i=0; fb=W*H*3
while True:
    buf = dec.stdout.read(fb)
    if len(buf) < fb: break
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    x = img.astype(np.float32)/255.0
    o = sess.run(None, {"src": x.transpose(2,0,1)[None], "r1i":rec[0],"r2i":rec[1],"r3i":rec[2],"r4i":rec[3],"downsample_ratio":dsr})
    pha = o[1][0,0]; fgr = o[0][0].transpose(1,2,0); rec = o[2:6]
    i += 1
    if i <= start - s0: continue
    a = cv2.GaussianBlur(pha, (0,0), 1.2)[..., None]
    # ---- background: fill subject, blur (depth), darken, cool/brand tint
    small = cv2.resize(img, (W//4, H//4), interpolation=cv2.INTER_AREA)
    m = (cv2.resize(pha, (W//4, H//4)) > 0.2).astype(np.uint8)*255
    m = cv2.dilate(m, np.ones((9,9), np.uint8))
    fill = cv2.inpaint(small, m, 5, cv2.INPAINT_TELEA)
    fill = cv2.GaussianBlur(fill, (0,0), 2.2)
    bg = cv2.resize(fill, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32)/255.0
    lum = bg.mean(axis=2, keepdims=True)
    bg = lum + (bg - lum)*0.72                      # desaturate
    bg = bg * np.array([0.96, 0.99, 1.03], np.float32) # cool toward brand blue
    bg = curve(bg, 0.0, 0.74, 1.10) * (0.62 + 0.38*vig)  # darken + vignette
    # ---- subject: key light + contrast + gentle warmth
    fg = np.where(pha[...,None] > 0.97, x, fgr)  # de-spilled edge colours
    fg = curve(fg, 0.01, 1.0, 1.04)                 # lift shadows a touch
    fg = fg + key*0.08*(1-fg)                          # key light (screen, no clipping)
    fg = fg * np.array([1.015, 1.0, 0.985], np.float32) # warm skin
    c = 0.45; fg = np.clip((fg - c)*1.10 + c, 0, 1)    # contrast
    fg = fg * (0.88 + 0.12*side[..., None])          # fill side falls off (modelling)
    # ---- rim light: edge band on subject, stronger on camera-right
    er = cv2.erode((pha>0.5).astype(np.uint8), np.ones((9,9),np.uint8)).astype(np.float32)
    rim = np.clip(pha - cv2.GaussianBlur(er,(0,0),3), 0, 1)
    rim = cv2.GaussianBlur(rim, (0,0), 2.0)[..., None] * (0.15 + 0.85*(1-side[..., None])) * np.clip((0.55*H-yy)/(0.25*H),0,1)[..., None]
    fg = fg + rim * np.array([0.78, 0.90, 1.0], np.float32) * 0.10
    outf = fg*a + bg*(1-a)
    enc.stdin.write((np.clip(outf,0,1)*255 + 0.5).astype(np.uint8).tobytes())
    if len(sys.argv) > 5 and sys.argv[5] == "--debug" and (i-(start-s0)) == 1:
        cv2.imwrite(out+"_alpha.jpg", (pha*255).astype(np.uint8))
enc.stdin.close(); enc.wait()
print("frames", i-(start-s0), "sec", round(time.time()-t0,1))
