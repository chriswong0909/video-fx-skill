# 聲效混音（sounds/ 聲效庫）

## 1. 聲效庫結構
- `sounds/SFX-###-slug/`：`sound.md`（front matter：id, name, name_en, category, duration, volume, mood, video_types, pace, pairs_with, source, license, learned, used_in, status）、`sound.mp3`、`peaks.json`（網頁波形用）。
- 類別：whoosh 轉場風聲｜pop 彈出｜ui 介面｜ding 提示音｜impact 重擊｜riser 張力｜foley 擬音｜accent 點綴｜music 背景音樂｜ambience 環境聲
- SFX 編號同 FX 分開；移除嘅寫入 `sounds/REMOVED.md`，編號唔重用。
- `registry.json` 嘅 `sounds` 陣列有全部摘要；揀聲效先睇佢，唔使逐個讀 sound.md。

## 2. 入庫
- 內置合成：`python3 tools/sfx.py synth`（已存在會略過；`--force --only SFX-00X` 重做）。
- 外來聲效（Pixabay、Mixkit 等免版稅）：`python3 tools/sfx.py add <檔> <slug> <category> "<中文名>" --start 0.2 --dur 1.0 --source "<網址>" --license "<授權>"`，然後補完 sound.md 嘅 mood、pairs_with、幾時用。**授權唔清楚嘅唔入庫。**
- 唔好由參考片抽聲效（人聲音樂混埋、版權屬原作者）；參考片只記錄「幾時落聲」，寫喺 analysis.md 嘅聲效欄。
- 入庫後 `node scripts/build-registry.mjs && node scripts/build-gallery.mjs`，重新發佈效果目錄。

## 2b. 聲效包（Kenney CC0）
- `sounds/PACKS.md` 列出每個包嘅來源同授權；sound.md 有 `pack`、`curated`、`source_file`、`license`。
- 揀聲效優先次序：精選（curated，有 pairs_with）→ Kenney 擬音（kenney-casino 紙卡、kenney-rpg 翻書／開門、kenney-impact 撞擊）→ 其他。
- Kenney 短音樂（kenney-jingles）只用喺片頭片尾 1–3 秒，唔好當背景音樂 loop（我哋唔做 BGM）。
- 匯入新包：`python3 tools/import_pack.py <資料夾> <pack-slug> --license "..." --source "..."`（授權唔清楚唔匯入）。

## 3. 點樣落聲
- 對準**畫面動作**：接觸格、出現格、推鏡最快嗰格；唔係對準句子開頭。whoosh 嘅聲音中心喺約 40% 位，所以要早 0.3 秒落。riser／suck-in 要喺動作之前開始，完結一刻 = 畫面出現。
- 密度：口播片平均每 3–5 秒最多 1 個；同一個聲效每 60 秒最多 3 次；ding 全片 1–3 次。
- 講者講緊重點字嗰刻唔好落大聲效；放喺停頓位或者字尾。
- 醫療嚴肅題材：避免 error-buzz、glitch、sparkle；用 pop-soft、card-slide、whoosh-soft、ding。

## 4. 混音（原聲音量不變）
1. 分鏡 JSON 每鏡加 `sfx`：`[{"sfx":"SFX-001","t":3.8,"vol":0.35}]`（t 係全片時間）。
2. 草稿階段可以喺 HyperFrames 加 `<audio data-start data-duration data-track-index data-volume src>` 試位。
3. 正式版一律用：
   ```
   python3 tools/sfx.py mix source.mp4 cues.json mix.m4a
   ffmpeg -i render.mp4 -i mix.m4a -map 0:v:0 -map 1:a:0 -c:v copy -c:a copy -shortest out.mp4
   ```
   `mix` 用 amix normalize=0（人聲保持 1.0）+ alimiter 防爆音。**有聲效就唔再係原音軌 md5**，要同使用者講明音軌已加聲效。
4. 建議音量：sound.md 嘅 `volume`（0.3–0.5）；人聲講嘢時聲效再壓低。**唔做背景音樂**——用戶上 IG 時自己加，片入面有 BGM 會同 IG 音樂撞。
5. 核對：用手機喇叭同耳機各聽一次；`ffmpeg -i out.mp4 -af volumedetect` 確認 max_volume < -0.5 dB。

## 聲效對動作（2026-09-30，用戶話聲效同特效唔夾之後定）
做法跟教學包 short-form-edit：**先有視覺事件表，再配聲**；聲效「最響位」對準動作落地嗰格（唔係效果開始、唔係聲效檔開頭）。
1. 分鏡／composition 出 `sfx-events.json`：`[{"t": 落地秒數, "sfx": ..., "vol": ..., "why": ...}]`
2. `python3 tools/sfx_plan.py sfx-events.json sfx-cues.json`：自動量每個聲效最響位，t_開始 = t_落地 − peak
3. `python3 tools/sfx.py mix source.mp4 sfx-cues.json mix.m4a`

| 動作 | 落地時間（相對效果開始） | 聲 | 音量 |
|---|---|---|---|
| 大字撞入（scale 1.7→1） | +0.22 | SFX-011 低頻重擊 | 0.28–0.45 |
| 彈出（back.out 0.35s） | +0.20–0.25 | SFX-004／005 pop | 0.30 |
| bar／卡片滑入到位 | +0.30–0.40 | SFX-014 card-slide（大卡）／SFX-006 click（細 bar） | 0.30–0.35 |
| 鏡頭移動（拉闊／推近） | 移動中段 | SFX-001 whoosh-soft | 0.30 |
| 劃交叉／劃線 | 每一劃完 | SFX-087／089 scratch（兩劃用唔同聲） | 0.40 |
| 正面結論字 | +0.25 | SFX-008 ding（全片 ≤ 2 次） | 0.30 |
| 收尾 | +0.25 | SFX-009 chime-up | 0.30 |
| 開場預備 | 0 | SFX-015 心跳 | 0.50 |
- 硬切（全屏圖直接切入）**唔落聲**；連續兩張圖只喺第一張落。
- 同一組側邊標籤只喺第一個落聲；兩個聲相隔要 ≥ 0.15 秒。
- 我聽唔到聲：只可以保證時間對準，最後要用戶聽一次確認。

## 多把聲要平衡聲量（2026-10-02，黎青龍護肝篇，用戶要求）
訪問片換咗新 VO／旁白，或者一條片有多過一把聲（講者原聲、VO、第二位講者）：**出草稿之前一定要逐段對齊響度**，唔好靠整條 loudnorm。
- 實測：教授原聲 -25.5 LUFS，新 VO -26 至 -30 LUFS，而且 VO 八條問題之間相差 4.5 dB；整條 loudnorm 只會拉平平均數，條條問題仍然忽大忽細。
- 做法：每把聲出一條同長度嘅 48k mono wav（唔屬於佢嘅時間靜音，只做高通／輕降噪，**唔好做 loudnorm**），每條答案／每條問題一段：
  `python3 tools/level_match.py mix.wav --target -16 t_spk.wav:seg_spk.json t_vo.wav:seg_vo.json`
  工具逐段量 integrated LUFS → 加減 dB 去 -16 → 相加 → 軟限幅 -1.5 dBFS，並印出每段前後數值。
- 核對：混音後逐段再量一次，全部要喺目標 ±0.5 LU 之內；峰值 < -1 dBFS。數值寫入交片報告。
- 之後先用 `sfx.py mix` 疊聲效（聲效音量係相對 -16 LUFS 人聲定嘅）。
- 我聽唔到聲：只可以保證數值對齊，音色／遠近感差異要用戶聽。
