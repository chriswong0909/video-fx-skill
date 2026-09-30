# 節拍表 + 關鍵格靜圖關卡（render 前批核）

**點解：** 靜圖幾乎唔使錢、幾秒出到；成條片 render 要幾分鐘，仲要傳檔。
以前要 render 完先發現「0:00 對唔上」「名牌太大」「交叉同字同色」，而家喺呢關就捉到。

## 流程位置
```
分鏡確認 → 素材 → build（index.html + manifest）→ QA 三件套 → ★ 節拍表 + 關鍵格 ★ → 用戶批 → 草稿 render
```

## 做法
1. manifest 每項加 `comp`（零件）、`state`（hero 狀態）、`enter`（入場文法）、`beat`（hook/setup/tension/proof/turn/payoff）。
2. 原片抽格（每秒 10 格，已有就唔使再抽）：`ffmpeg -i graded.mp4 -vf fps=10,scale=540:-2 frames/f_%04d.jpg`
3. `node scripts/keyframes.cjs <proj> frames kf`（自動每個畫面字一格；或者俾時間 `3.2,9.8,…`）
4. `python3 tools/beatgrid.py manifest.json chars.json kf beatgrid.html sfx-events.json --title "<片名> 節拍表"`
5. 用 Artifact 發佈（同一專案同一連結），問用戶：「確認節拍表？邊行要改？」**停低等答覆。**
6. 用戶改 → 只改 build 腳本對應嗰行，重出受影響嗰幾格，唔好成份重做。

## 用戶睇緊乜
- 每一拍：講緊邊句、出咩字、屬邊款零件、點入場、配咩聲。
- 關鍵格：實際位置、大細、顏色（同成片一樣，因為係同一份 index.html）。
- 一眼睇晒全片用咗幾多款零件：`零件·狀態` 一欄應該只得系統卡嗰幾款。
